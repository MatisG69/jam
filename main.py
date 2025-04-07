import pygame
import random
import sys

# === التهيئة ===
pygame.init()
عرض, ارتفاع = 1920, 1080
نافذة = pygame.display.set_mode((عرض, ارتفاع))
pygame.display.set_caption("مستوحى من")
الساعة = pygame.time.Clock()

# === تحميل الموسيقى ===
pygame.mixer.music.load("موسيقى.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0)

# === الألوان ===
أبيض = (255, 255, 255)
أسود = (0, 0, 0)
لون_الأرض = (20, 20, 20)
أزرق = (0, 0, 255)
ذهبي = (255, 215, 0)

# === تحميل الصور ===
def تحميل_صورة(مسار, حجم):
    try:
        صورة = pygame.image.load(مسار).convert_alpha()
        return pygame.transform.scale(صورة, حجم)
    except:
        print(f"خطأ: الصورة مفقودة - {مسار}")
        pygame.quit()
        sys.exit()

خلفية_القائمة = تحميل_صورة("موضوعية.png", (عرض, ارتفاع))  # صورة الخلفية للقائمة
خلفية = تحميل_صورة("موضوعية.png", (عرض, ارتفاع))
صورة_اللاعب = تحميل_صورة("شخصية.png", (60, 60))
صورة_العائق = تحميل_صورة("وحش.png", (80, 80))
صورة_القطعة = تحميل_صورة("غرفة.png", (60, 60))
صورة_إيستر = تحميل_صورة("مجلس الطلبة.png", (400, 400))  # صورة للـ Easter egg

# === اللاعب ===
موقع_اللاعب_x = 100
موقع_اللاعب_y = ارتفاع - 110
سرعة_اللاعب_y = 0
الجاذبية = 1
قوة_القفز = -18
على_الأرض = True
مستطيل_اللاعب = pygame.Rect(موقع_اللاعب_x, موقع_اللاعب_y, 60, 60)

# === الكائنات الديناميكية ===
العوائق = []
القطع = []
سرعة_اللعبة = 8

# === النتيجة ===
النتيجة = 0
الخط = pygame.font.SysFont("Arial", 36)

إيستر_مفعل = False
وقت_إيستر = 0
مدة_إيستر = 3000

# === الدوال ===
def إعادة_البدء():
    global العوائق, القطع, النتيجة, موقع_اللاعب_y, سرعة_اللاعب_y, سرعة_اللعبة
    العوائق.clear()
    القطع.clear()
    النتيجة = 0
    موقع_اللاعب_y = ارتفاع - 110
    سرعة_اللاعب_y = 0
    سرعة_اللعبة = 8

def رسم_النافذة():
    نافذة.blit(خلفية, (0, 0))
    pygame.draw.rect(نافذة, لون_الأرض, (0, ارتفاع - 50, عرض, 50))
    نافذة.blit(صورة_اللاعب, مستطيل_اللاعب)

    for عائق in العوائق:
        نافذة.blit(صورة_العائق, عائق)
    for قطعة in القطع:
        نافذة.blit(صورة_القطعة, قطعة)

    # النتيجة
    نص_النتيجة = الخط.render(f"Punteggio: {النتيجة}", True, أبيض)
    نافذة.blit(نص_النتيجة, (عرض - 200, 30))

    # تلاشي الصورة
    if إيستر_مفعل:
        ألفا = max(0, 255 - int((pygame.time.get_ticks() - وقت_إيستر) / مدة_إيستر * 255))
        if ألفا > 0:
            سطح_إيستر = صورة_إيستر.copy()
            سطح_إيستر.set_alpha(ألفا)
            نافذة.blit(سطح_إيستر, (عرض // 2 - 100, ارتفاع // 2 - 100))

    pygame.display.update()

def ظهور_العائق():
    مستطيل = pygame.Rect(عرض, ارتفاع - 110, 60, 60)
    العوائق.append(مستطيل)

def ظهور_القطعة():
    مستطيل = pygame.Rect(random.randint(عرض, عرض + 100), ارتفاع - 150, 40, 40)
    القطع.append(مستطيل)

def عرض_القائمة():
    خط_القائمة = pygame.font.SysFont("Arial", 50)
    نص_البدء = خط_القائمة.render("Premi [Spazio] per giocare", True, ذهبي)
    نص_الخروج = خط_القائمة.render("Premi [ESC] per uscire", True, ذهبي)

    # خلفية القائمة
    نافذة.blit(خلفية_القائمة, (0, 0))

    # عرض النصوص
    نافذة.blit(نص_البدء, (عرض // 2 - نص_البدء.get_width() // 2, ارتفاع // 2 - 100))
    نافذة.blit(نص_الخروج, (عرض // 2 - نص_الخروج.get_width() // 2, ارتفاع // 2 + 50))

    pygame.display.update()

def اللعبة():
    global موقع_اللاعب_y, سرعة_اللاعب_y, على_الأرض, النتيجة, إيستر_مفعل, وقت_إيستر, سرعة_اللعبة
    العوائق.clear()
    القطع.clear()
    النتيجة = 0
    موقع_اللاعب_y = ارتفاع - 110
    سرعة_اللاعب_y = 0
    سرعة_اللعبة = 8

    وقت_ظهور_العائق = 0  # التصريح هنا
    وقت_ظهور_القطعة = 0  # التصريح هنا
    جاري_التشغيل = True
    خسارة = False

    while جاري_التشغيل:
        dt = الساعة.tick(60)
        الوقت_الحالي = pygame.time.get_ticks()

        for حدث in pygame.event.get():
            if حدث.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if حدث.type == pygame.KEYDOWN:
                if حدث.key == pygame.K_SPACE and على_الأرض:
                    سرعة_اللاعب_y = قوة_القفز
                    على_الأرض = False
                if حدث.key == pygame.K_r:
                    اللعبة()
                if حدث.key == pygame.K_a and not إيستر_مفعل:
                    إيستر_مفعل = True
                    وقت_إيستر = pygame.time.get_ticks()
                if حدث.key == pygame.K_ESCAPE:
                    جاري_التشغيل = False

        سرعة_اللاعب_y += الجاذبية
        موقع_اللاعب_y += سرعة_اللاعب_y
        if موقع_اللاعب_y >= ارتفاع - 110:
            موقع_اللاعب_y = ارتفاع - 110
            سرعة_اللاعب_y = 0
            على_الأرض = True
        مستطيل_اللاعب.y = موقع_اللاعب_y

        # ظهور العوائق والقطع
        if الوقت_الحالي - وقت_ظهور_العائق > 1500:
            وقت_ظهور_العائق = الوقت_الحالي
            ظهور_العائق()
        if الوقت_الحالي - وقت_ظهور_القطعة > 2000:
            وقت_ظهور_القطعة = الوقت_الحالي
            ظهور_القطعة()

        # حركة الكائنات
        for عائق in العوائق:
            عائق.x -= سرعة_اللعبة
        for قطعة in القطع:
            قطعة.x -= سرعة_اللعبة

        # التصادم
        for عائق in العوائق:
            if مستطيل_اللاعب.colliderect(عائق):
                إعادة_البدء()
                return

        for قطعة in القطع[:]:
            if مستطيل_اللاعب.colliderect(قطعة):
                القطع.remove(قطعة)
                النتيجة += 10

        # إزالة الكائنات التي خرجت من الشاشة
        العوائق[:] = [عائق for عائق in العوائق if عائق.x > -80]
        القطع[:] = [قطعة for قطعة in القطع if قطعة.x > -60]

        # زيادة الصعوبة تدريجيًا
        if النتيجة > 0 and النتيجة % 100 == 0:
            سرعة_اللعبة += 0.5

        رسم_النافذة()

def الرئيسية():
    جاري_التشغيل = True
    while جاري_التشغيل:
        عرض_القائمة()
        for حدث in pygame.event.get():
            if حدث.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if حدث.type == pygame.KEYDOWN:
                if حدث.key == pygame.K_SPACE:
                    اللعبة()  # بدء اللعبة
                if حدث.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

الرئيسية()
