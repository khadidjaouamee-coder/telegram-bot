import telebot
from telebot import types
import random
from flask import Flask
from threading import Thread

# ===========================================
# 👇 ضع التوكن الخاص بك هنا
# ===========================================
TOKEN = "8904537116:AAE0eaj2IbO5oHNQfkJ6RVYJy6DoY36UjRc"
bot = telebot.TeleBot(TOKEN)

# ========== إنشاء تطبيق Flask للويب ==========
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ البوت يعمل بشكل طبيعي!"

# ===========================================
# البيانات: التلاوات + الكتب (أقسام العقيدة، الفقه، أخرى)
# ===========================================
DATA = {
    "recitations": [
       "CQACAgQAAxkBAAMhaiAGsmlQW3u2wdwlcpHs8yaLdskAAkUcAALPbmBTmwWs6sOVLcQ7BA",
       "CQACAgQAAxkBAAICHWoh3QRwm4x6rdjGMj-dbOEF33bVAAJaHgACaDD4Ugw8rJKeTriYOwQ",
       "CQACAgQAAxkBAAMdaiAF05xpPyCud9P04Nm-wrlHsskAAqkcAAJKeFFTSKemi14cK7Q7BA",
       "AwACAgIAAxkBAAMYaiACwUPlt-iM20J6hnIBI0RcYHcAAqCeAAI0jZhLvGMEQ8wu6Hs7BA",
       "AwACAgIAAxkBAAMfaiAGoLmkh5bOuWwjzM0LQcTpCwkAAiRhAALFrIFLQD2jnhyIfdc7BA",
       "CQACAgQAAxkBAAOyaiBHb52oFU51oeFXeeE0qTRbvc8AAn0IAAI68rhRJhyIyqBleVE7BA",
       "CQACAgQAAxkBAAIBFmogkAzaVadALzu-KVp7CgAB_QjriQACeAgAAmHhgFPAQmhK8xu4yTsE",
       "CQACAgQAAxkBAAOwaiBGBg1sazrruYQU_3ff9zOG2KcAAgQHAALy2RhSlWDePw6lrw07BA",
       "CQACAgQAAxkBAAIBGGogkAzpeDfxH9Sr2XISe5PAv4YxAAKKCAACq6zIU-OeXfX_Tt70OwQ",
       "CQACAgQAAxkBAAIBGWogkAwUYPahNQOV57KYYinv51pVAAKOCAACq6zIUxQwUQLfiN8AATsE",
       "CQACAgQAAxkBAAIBGmogkAzdYZwUdAyKjrZOj-eyeAXwAAKQCAACq6zIU1Xtm8R1SrTUOwQ",
       "CQACAgQAAxkBAAIBG2ogkAzaZdt5TXGDg_J8XbuaCT_EAAKXCAACq6zIU9LDTsUWMPoSOwQ"
    ],

    "selected_audios": [     
        "CQACAgQAAxkBAAIBj2oheniMS8JaP7AEfA-JZvbsyEsWAALFFwACJ4cxUkz7WUDjexJSOwQ",
        "CQACAgQAAxkBAAIBkGohenjh97VuHCYHHfJz7uCth9WiAALaJQACrH-gUDqJFtESgJoUOwQ",
        "CQACAgEAAxkBAAICTGoh4d9QI3IRLOK-nTLLqRWMpn-_AAJnBgACn_OARCGi7NzRoMgxOwQ",
        "CQACAgUAAxkBAAIBpWohenj032q6t4WQFNUtSHT60_xRAALxEwACMMaAVZdcSNZM4xHrOwQ",
        "CQACAgQAAxkBAAICSmoh4d9zIpRd2LTXbIRA0H0qjHwUAAJeIAACnCSgUO5VWeqX9V2IOwQ",
        "CQACAgIAAxkBAAICSWoh4d9YdsUNuEmM5T3rQmodKDikAAKsmgAC07y5SCKN_c2GMpKrOwQ",
        "CQACAgUAAxkBAAICfWoh48cRicCmAAFrOLjdFIl92NpsKwACmRMAAmaL0FaUNLKNnwsxqzsE",
        "CQACAgIAAxkBAAICfGoh48ebzfxqRZuBdM1ykeUeoyS0AAIprQACVkBZSSfsYw7cg0qROwQ",
        "CQACAgQAAxkBAAICcmoh48eLAixIm8PmxIEvcNBAOk9kAAKMGgAC2sj5UidKJCd2gtXWOwQ",
        "CQACAgIAAxkBAAICcWoh48eFMCEnT0Ii99RoV9AGeBMQAALEdgACm4_ISdnK2vTuyWLkOwQ",
        "CQACAgQAAxkBAAICcGoh48fllUlcfzligNiDWbeXZ9oyAAKIdgACaXQQUUfy7Nar-gLqOwQ",
        "CQACAgIAAxkBAAICb2oh48dhjGqWdyxixi4OM05l0y7BAAI4TQAC_HgZSwWcemXbsAVBOwQ",
        "CQACAgQAAxkBAAICbmoh48e9t9FtBYwLEY3O2aTvctNgAAJDGAACVAK5UEEhRcy47tBBOwQ",
        "CQACAgQAAxkBAAICbWoh48eztx3SOErgbdodjOhI7qWiAALLHQACsPqQUFQJbG3Co61xOwQ",
        "CQACAgQAAxkBAAICbGoh48dHcpMoCDfHMbJAN5hAli1QAAJzEgACt1RAUpBzP3gD24m9OwQ",
        "CQACAgQAAxkBAAICa2oh48e0TPPeKZYM2t-w1A_bstxMAAIYGgAC7R7AU9hysxNHPoQ7OwQ",
        "CQACAgIAAxkBAAICe2oh48edCbSJNSleZNH47ARfkEA4AAKDVQACgV-QSD7iiHdAw5w4OwQ",
        "CQACAgQAAxkBAAICemoh48e7NraMw0C563Sx2wTkMRvXAAMWAAKx6_lQEG3atS6V_xQ7BA",
        "CQACAgQAAxkBAAICZGoh48cWAptd8ST6LYXUftpd7UL7AAKpGAACMh7ZUFaRNoZD_vSFOwQ",
        "CQACAgQAAxkBAAICVWoh48eL-T0SMvR9xj1k-0GcwVPqAAIwGgACsfcAAVCVlMMusv1jRzsE",
        "CQACAgQAAxkBAAICSGoh4d8QY9_jouxISovJY6YxATB8AALPEwAC4GgYUHVcsx8aUrqFOwQ",
        "CQACAgQAAxkBAAICR2oh4d83T--MnXXlmEYNqfFgYN5BAAK-EgACJfl4UUClnZf1MhmUOwQ",
        "CQACAgQAAxkBAAICRmoh4d_RKaYWJF02vSJgCUCFc4UEAAKtEgAC4MHYUIcL4HbwT7FkOwQ",
        "CQACAgQAAxkBAAICWWoh48e2NfwAAQ36WTtdzqu9i1-bHQAC-BYAAhlFOVDSN64F_wjgnzsE",
        "CQACAgQAAxkBAAICWGoh48fFr4BiuFd-UMz_-DfmCwkHAALQGwACyRGwUP07qvtAZw8HOwQ",
        "CQACAgQAAxkBAAICV2oh48eMkohlIEPaqsHl8eQGgQ6bAAKaHAACCM-oUGu91dGigdmUOwQ",
        "CQACAgQAAxkBAAICVmoh48cxDEIYBz3DMVfEfeveSlz5AAIpHQAC-E1IUBW2sYcCtfjyOwQ",
        "CQACAgQAAxkBAAICNWoh4d8Bsfdh9raZkYuAo1y4xTsVAAL9CQACb7XAUlcQUhx7PoetOwQ",
        "CQACAgQAAxkBAAIBkWoheniFj4xmzOT1kw1jc939WIqGAAKJHgACyMfhUL_UNucf9RA1OwQ",
        "CQACAgQAAxkBAAIBkmohengiS7svrRaM4hBL_dcdIIWZAAKLGQACZLiZUCKp73vXy8uAOwQ",
        "CQACAgQAAxkBAAIBk2ohenjTgiR_oPpcUoSoNDtQ2s2KAAKgGwACM27JUSXzPRfC_bX8OwQ",
        "CQACAgIAAxkBAAIBm2ohenguhBkDjIpzQMLSrYzKIalYAAK3hwACdMOoSCHPsK9At12xOwQ",
        "CQACAgQAAxkBAAIBnGohenhfYpbvXFAhbfZ3e-hT4mVUAAKjIgACjKDZUBEN-rJB_iXgOwQ",
        "CQACAgQAAxkBAAIBnWohengT9ciB1RuFliqo37LFB33hAAJQHgAC8p6QUVpb11f0aIW3OwQ",
        "CQACAgQAAxkBAAIBnmohenj1nyK6tM6JR4Kxk1s5FLOZAAJFGwAChr-wUb4uDPaVFlLZOwQ",
        "CQACAgIAAxkBAAIBn2ohenjfplIxtlmYl2O0t_18l-_GAALXAgAC9efwSVyAQjr0oLTZOwQ",
        "CQACAgIAAxkBAAIBoGoheng8_WYO2L-f7dJ4LJcoL2CyAALEhgACVg8JSPIBEeTVub2zOwQ",
        "CQACAgIAAxkBAAIBoWoheni6w1Nv2t0Bz85ZvKKq31ZgAAIxsAACcTLpSkbr7L8gVwV1OwQ",
        "CQACAgIAAxkBAAIBomohenh2vT3MekgPptyUMjhTZSsbAAJIsAACcTLpSiTMQTEuJidHOwQ",
        "CQACAgQAAxkBAAIBo2ohengC9JIdUdcwSiUKAAEUNNVGEwACSRsAAqKPaVJ9_MXdMGJmIDsE",
        "CQACAgUAAxkBAAIBpWohenj032q6t4WQFNUtSHT60_xRAALxEwACMMaAVZdcSNZM4xHrOwQ",
        "CQACAgIAAxkBAAICgmoh48eohNbzy8qjW09Utd2ipXcvAAJvQgACkD2YShqczAMz9AYrOwQ",
        "CQACAgQAAxkBAAICgWoh48f7teHNSBxEihLGoIcFFz0FAAJ4EAACd-rJUNk_IVI9s-AlOwQ",
        "CQACAgIAAxkBAAICgGoh48fth1JGQBndt1txqw_cQh-_AAIJzgACik9BSI4tWUQfP3l-OwQ",
        "CQACAgQAAxkBAAICf2oh48dyzd6GaQ7dHF9KWJHXhis3AAKYGwACM724US8guDr33yR2OwQ",
        "CQACAgQAAxkBAAICfmoh48d8pDL8WPsGqE9ghVj0hQoWAAIXDgACL9XBU-7-Ii-GutOvOwQ",
        "CQACAgQAAxkBAAIBlGohenj-kpr9NQejXIxdO9Qc04lEAAKIGwACY7DRUX2Vo10OImB3OwQ",
        "CQACAgQAAxkBAAIBlWohenjh4yor4Kusv3a-AVZjOGzRAAJHGgAC4zQxUkU5tNDrfmy1OwQ",
        "CQACAgQAAxkBAAIBlmohengpcHuoCZAFMCJ6StSXkXYCAALGGAACbaaZUjPvV2L21B5wOwQ",
        "CQACAgQAAxkBAAIBl2ohenifucgVdnYfZHMEfKuFtLXIAAJTAwACOFngBz4h3EACNimcOwQ",
        "CQACAgQAAxkBAAIBmGohengnvwYI773hVxIzAwErW72bAAKKHQACqUdhUI4u8T_DqX0pOwQ",
        "CQACAgQAAxkBAAIBmWohengogEL_ZOiZSJjAA-hji2e8AAKkGwACV8WAUHFmVqPw7x0zOwQ",
        "CQACAgIAAxkBAAIBmmoheniiHPhOusIMlDz2LIpR7BM7AAI5jQACzYWhSOgXoXhJ5xfoOwQ",
        "CQACAgQAAxkBAAICd2oh48e465lkb8barJJrVfUUaM7CAAKvAAO_w8QJLP_z1AT5pjI7BA",
        "CQACAgQAAxkBAAICdmoh48dUIzX0pvMZrunCaDDtVFNvAAL6FwAC1u2AUhFA7_42GZzOOwQ",
        "CQACAgQAAxkBAAICc3oh48euGDopNkMnkt22ikSgGa3xAAIVEgACwBXpUIPW6GQAAQx6eTsE",
        "CQACAgQAAxkBAAICamoh48fwS0lruZj2egsOIQav2Ye1AAIPGAACXk-JU8F52ZFoff-5OwQ",
        "CQACAgQAAxkBAAICaWoh48dCvHVERCzGJt1gH3-pmh0lAALBGwAC1b54U9ZM-CHBVp_kOwQ",
        "CQACAgQAAxkBAAICaGoh48choY1HA0zRzSrNchBAN8o5AAL-BgACrRMhUIVHjJbDYQ0SOwQ",
        "CQACAgQAAxkBAAICZ2oh48dBm5drXpLb9q5gFH7ECdrmAAKGGgACCnhBUa86QD94Qtl_OwQ",
        "CQACAgUAAxkBAAICZmoh48csxXkuPzxxPcwnhAoytFB2AALtHgACNw_gV3aKuAAB98ceazsE",
        "CQACAgIAAxkBAAICZWoh48f2HkMpicKwYYWi9od982dzAAJEiAACfTlYSlRN18dEodxEOwQ",
        "CQACAgQAAxkBAAICZGoh48cWAptd8ST6LYXUftpd7UL7AAKpGAACMh7ZUFaRNoZD_vSFOwQ",
        "CQACAgQAAxkBAAICY2oh48euvSyLFGPQpmpSsDVieZt4AAJiLQAC67BZUv7DftZmDvE6OwQ",
        "CQACAgQAAxkBAAICYmoh48e0OQQhRmR7NzYInzGF2fDKAAKcGQACK8dJUv2MMpPEsxQCOwQ",
        "CQACAgQAAxkBAAICYWoh48flMQdkfcEhnjuvzfs-ranRAAJREwACR-sxUUOsBWTwM3FvOwQ",
        "CQACAgQAAxkBAAICYGoh48fzSz8oEZqeMxgOIuobAy3cAAJoGAACsDowUru3vAKy8wNFOwQ",
        "CQACAgQAAxkBAAICX2oh48dgCLhCwkeHt7vhZYhsFESDAAKUGQACosIAAVL7J2Zd5P1ZKzsE",
        "CQACAgQAAxkBAAICXmoh48f-mTiCjz9QNpyuvxETVEHMAALlDwACKFbxUTF-Bd3GW8PBOwQ",
        "CQACAgUAAxkBAAICXWoh48cqCrvfsSoO05falncMY2LkAAK4FAACD8V4Vs9b61Cy1dVEOwQ",
        "CQACAgQAAxkBAAICXGoh48cqoz1G6mTUqS2VKpkrInZ-AALhFwAC_jvpUCDnsRcXvNLoOwQ",
        "CQACAgQAAxkBAAICW2oh48fVgRaQUAp-J5ILP-9elhONAAJSHgACQP-BUGqyqztUzf7JOwQ",
        "CQACAgQAAxkBAAICWmoh48dVcuH__7GUoOibOs_Cj6b5AAKwEQACmHGJUskS8oiE697eOwQ",
        "CQACAgIAAxkBAAIBpmohenj23jYkjst9r_y_QULn_BQBAAKVnwACcTLpSnh7-TQc-C10OwQ"
    ],

    # ========== دورات العقيدة (أزرار تفاعلية) ==========
    "courses_aqida": {
        "متون التوحيد وأصول الإيمان المستوى الأول": "https://t.me/mtoon_altawheed",
        "برنامج الأشبال العلمي - الشيخ عبد الرزاق البدر": "https://t.me/Alashbal1"
    },

    # ========== دورات الفقه ==========
    "courses_fiqh": {
        "برنامج الفقه - الشيخ عبد الرزاق البدر": "https://t.me/fiqhalbadr"
    },

    # ========== دورات عامة ==========
    "courses_general": {
        "برنامج أعمال القلوب": "https://t.me/aemal_alqulub",
        "برنامج الآداب والأخلاق": "https://t.me/adab_akhlaq",
        "برنامج الأدعية والأذكار": "https://t.me/adeiat_adhkar"
    },

    # ========== كتب العقيدة ==========
    "books_aqida": {
        "🔹شرح الشيخ د.صالح بن فوزان الفوزان للأصول الثلاثة": "BQACAgUAAxkBAANGaiAeZlcTWbDpEhdGr161iubjT_MAAtgPAAJ6OfhWJxB_x22KH-g7BA",
        "🔹مذكرة في العقيدة للسحيمي": "BQACAgQAAxkBAANIaiAfL1g_B39-zMIwbmPUf9TxOHcAAuUhAAKPmwABUQNpOEzJItX0OwQ",
        "🔹كتاب العقيدة الصحيحة وما يضادها": "BQACAgQAAxkBAAPLaiBdlNYLPlRNOQpsxWVKt4DrO1AAAlIHAAK8PPlQPcWTjLpivSI7BA",
        "🔹متن العقيدة الواسطية": "BQACAgQAAxkBAAPNaiBdmwSW3H-2xcMf5ueDcl68GW4AAgUJAAIjrmlSU5pXoJlPjSY7BA",
        "🔹شرح العقيدة الواسطية": "BQACAgQAAxkBAAPPaiBdpHzGvUwzGFYJzb0nx0-CwekAAqAUAAKQSZBTcdKflTMYmEQ7BA",
        "🔹كتاب: من فتاوى العقيدة": "BQACAgQAAxkBAAPVaiBfb4dsGC3wPYVu92vXw6SSe-wAAj4fAAIiEJFSCUEzWf5iRSk7BA",
        "🔹كتاب معنى كلمة التوحيد": "BQACAgQAAxkBAAPXaiBfgr-vujmlyp5rEgWrLmlHM4UAAqwYAAL3rolQlo2x3zvtX9Q7BA",
        "🔹كتاب الجامع لأحكام المرأة المسلمة": "BQACAgQAAxkBAAPaaiBf0V2yLRo_5SYAAbZZw_tw7MHFAAKTGQACrLSQUqMxplLorqaeOwQ"
    },

    # ========== كتب الفقه ==========
    "books_fiqh": {
        "صفة صلاة النبي ﷺ 📘": "BQACAgQAAxkBAAIBVWohaHwv5KhBBXt5VDwAAXcCIA6IqQACbR4AAp0RKVEMSgKxBAOBSzsE",
        "من فتاوى الطهارة والصلاة 📘": "BQACAgQAAxkBAAIBVGohaHwOf1C6DlUe60_1A8blUNfpAALiFgACLz6RUUVlEoQ2JcHPOwQ",
        "المسودة في أصول الفِقه لابن تيمية 📘": "BQACAgQAAxkBAAIBVmohaHxdQOa-lvUkP-JCZibYijitAAK4CAACKBFRUKZ5Icfert17OwQ",
        "الكافي في فِقه المدينة المالِكي 📘": "BQACAgIAAxkBAAIBU2ohaHzKI5apo2GHHsU7cducdJJ6AAKrhQACseXpSSemLE5Qy1UKOwQ"
    },

    # ========== كتب أخرى / متنوعة ==========
    "books_misc": {
        "وصايا ابن قدامة 📗": "BQACAgQAAxkBAAIBb2ohbgeT-aiDMiHgA9Kn5QxhpQ2pAAJ2GwACkzFBU0P6pG73i5TDOwQ",
        "أوقات وأحوال يُستجاب فيها الدعاء 📗": "BQACAgQAAxkBAAIBbmohbgfiV5MHjUNUFYK2ULbNByEEAAK-HQAC_l4RUewVgNzpfqiyOwQ",
        "المورد العذب الزلال فيما انتقد فيه بعض المناهج الدعوية 📗":"BQACAgQAAxkBAAIBbWohbgc1z84nLaLPptLC8SM9P9IpAAIaGwAC8O-RUnuEcdv6xmXsOwQ",
        "كَيف تغضّ بصرك للشيخ عبد الرزاق البدر 📗":"BQACAgQAAxkBAAIBbGohbgc08WsjDvsPdUipUnTRMP4dAAJRHgAC8p6QUSOwE7TUkhgKOwQ",
        "قصيدة في فضل أمّ المؤمنين عائشة 📗":"BQACAgQAAxkBAAIBa2ohbgd5qVsy-iAL0ywwXOQmxw9mAAIRGAACjISxUOYuePuJEOjsOwQ",
        "حِجابُكِ أيّتها المُسلِمة 📗":"BQACAgQAAxkBAAIBamohbgfiE0XA1hxb8z0-901GVd3_AAKrGwACEYHBUjiD3U4kCQvtOwQ",
        "دراسات في البدعة والمبتدعين 📗":"BQACAgQAAxkBAAIBZ2ohbgdiFnTgMPoqLkYJOZulRU-tAALvHAAC-npRUe1zcSj0YzqTOwQ",
        "دور المرأة في إصلاح المجتمع لابن عثيمين 📗":"BQACAgQAAxkBAAIBYWohbge2o7RMHdXMbbkx48PCD7gGAALMGQACRQKpU_wCkSfGSqOjOwQ",
        "منهج يومي لِطالب العلم_ابن عثيمين 📗":"BQACAgQAAxkBAAIBYGohbgfhsy9_x5u9UA3GoUwl99_SAAI2FwACQXDwUY2vMT9oCDaPOwQ",
        "المعصية وأثرها السيء على الأمة -للشيخ ربيع رحمه الله- 📗":"BQACAgQAAxkBAAIDq2onOBJsxOaWjTsAAUkbtNZsUd7LfgAC7Q0AArr2yVP9Th9uc2iCPDsE",
        "عوائق الطلب_بنُ بَرجس 📗":"BQACAgQAAxkBAAIBYmohbgevE7C7da_G7TUJQGftiJYcAAL2FQACh5TYU7udxFPmZ1IIOwQ"
    }
}

# ===========================================
# إنشاء اختصارات قصيرة لكل كتاب (لتجنب خطأ BUTTON_DATA_INVALID)
# ===========================================
book_shortcuts_aqida = {f"aqida_{i}": name for i, name in enumerate(DATA["books_aqida"].keys(), 1)}
book_shortcuts_fiqh = {f"fiqh_{i}": name for i, name in enumerate(DATA["books_fiqh"].keys(), 1)}
book_shortcuts_misc = {f"misc_{i}": name for i, name in enumerate(DATA["books_misc"].keys(), 1)}

# إنشاء اختصارات قصيرة للدورات (لتجنب خطأ BUTTON_DATA_INVALID)
course_shortcuts_aqida = {f"course_aqida_{i}": name for i, name in enumerate(DATA["courses_aqida"].keys(), 1)}
course_shortcuts_fiqh = {f"course_fiqh_{i}": name for i, name in enumerate(DATA["courses_fiqh"].keys(), 1)}
course_shortcuts_general = {f"course_gen_{i}": name for i, name in enumerate(DATA["courses_general"].keys(), 1)}

# ===========================================
# دوال القوائم (menus)
# ===========================================
def main_menu():
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_recitation = types.InlineKeyboardButton("🎧 تلاوة مختارة", callback_data="main_recitation")
    btn_audio = types.InlineKeyboardButton("🎙️ صوتية مختارة", callback_data="main_selected_audio")
    btn_books = types.InlineKeyboardButton("📚 كتب مفيدة", callback_data="main_books")
    btn_courses = types.InlineKeyboardButton("🎓 دورات مفيدة", callback_data="main_courses")
    markup.add(btn_recitation, btn_audio, btn_books, btn_courses)
    return markup

def books_category_menu():
    """قائمة أصناف الكتب (عقيدة، فقه، أخرى)"""
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_aqida = types.InlineKeyboardButton("🕌 كتب العقيدة", callback_data="cat_books_aqida")
    btn_fiqh = types.InlineKeyboardButton("⚖️ كتب الفقه", callback_data="cat_books_fiqh")
    btn_misc = types.InlineKeyboardButton("📖 كتب أخرى", callback_data="cat_books_misc")
    btn_back = types.InlineKeyboardButton("↩️ العودة للرئيسية", callback_data="back_to_main")
    markup.add(btn_aqida, btn_fiqh, btn_misc, btn_back)
    return markup

def courses_menu():
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_c_aqida = types.InlineKeyboardButton("🕌 دورات العقيدة", callback_data="sub_c_aqida")
    btn_c_fiqh = types.InlineKeyboardButton("⚖️ دورات الفقه", callback_data="sub_c_fiqh")
    btn_c_gen = types.InlineKeyboardButton("🌍 دورات عامة", callback_data="sub_c_gen")
    btn_back = types.InlineKeyboardButton("↩️ العودة للرئيسية", callback_data="back_to_main")
    markup.add(btn_c_aqida, btn_c_fiqh)
    markup.add(btn_c_gen)
    markup.add(btn_back)
    return markup

# ===========================================
# أوامر البوت ومعالجة الأزرار
# ===========================================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "مرحبًا بِك🌟\nاختر القسم الذي ترغب فيه:",
        reply_markup=main_menu()
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    print(f"[DEBUG] Received callback: {call.data}")
    bot.answer_callback_query(call.id)

    # 1. تلاوة مختارة
    if call.data == "main_recitation":
        try:
            random_audio = random.choice(DATA["recitations"])
            bot.send_audio(call.message.chat.id, random_audio, caption="🎧 تلاوة خاشعة تم اختيارها لكِ")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"⚠️ خطأ: {e}")

    # 2. صوتية مختارة
    elif call.data == "main_selected_audio":
        try:
            random_audio = random.choice(DATA["selected_audios"])
            bot.send_audio(call.message.chat.id, random_audio, caption="🎙️ مقطع صوتي مختار لكِ")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"⚠️ خطأ: {e}")

    # 3. كتب مفيدة - تظهر أصناف الكتب
    elif call.data == "main_books":
        bot.edit_message_text(
            "📚 اختر صنف الكتب:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=books_category_menu()
        )

    # 4. عرض كتب العقيدة
    elif call.data == "cat_books_aqida":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for code, name in book_shortcuts_aqida.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=code))
        markup.add(types.InlineKeyboardButton("🔙 العودة للأصناف", callback_data="main_books"))
        bot.edit_message_text("📚 كتب العقيدة:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # 5. عرض كتب الفقه
    elif call.data == "cat_books_fiqh":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for code, name in book_shortcuts_fiqh.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=code))
        markup.add(types.InlineKeyboardButton("🔙 العودة للأصناف", callback_data="main_books"))
        bot.edit_message_text("⚖️ كتب الفقه:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # 6. عرض الكتب الأخرى (متنوعة)
    elif call.data == "cat_books_misc":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for code, name in book_shortcuts_misc.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=code))
        markup.add(types.InlineKeyboardButton("🔙 العودة للأصناف", callback_data="main_books"))
        bot.edit_message_text("📖 كتب أخرى:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # 7. إرسال الكتاب المطلوب (بناءً على الاختصار)
    elif call.data.startswith("aqida_"):
        book_name = book_shortcuts_aqida[call.data]
        file_id = DATA["books_aqida"][book_name]
        bot.send_document(call.message.chat.id, file_id, caption=f"📖 {book_name}")
    elif call.data.startswith("fiqh_"):
        book_name = book_shortcuts_fiqh[call.data]
        file_id = DATA["books_fiqh"][book_name]
        bot.send_document(call.message.chat.id, file_id, caption=f"📖 {book_name}")
    elif call.data.startswith("misc_"):
        book_name = book_shortcuts_misc[call.data]
        file_id = DATA["books_misc"][book_name]
        bot.send_document(call.message.chat.id, file_id, caption=f"📖 {book_name}")

    # 8. دورات مفيدة - عرض أصناف الدورات
    elif call.data == "main_courses":
        bot.edit_message_text(
            "🎓 اختر مجال الدورة:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=courses_menu()
        )

    # 9. عرض قائمة دورات العقيدة (أزرار)
    elif call.data == "sub_c_aqida":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for code, name in course_shortcuts_aqida.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=code))
        markup.add(types.InlineKeyboardButton("🔙 العودة للأصناف", callback_data="main_courses"))
        bot.edit_message_text("🎓 **دورات العقيدة المتاحة:**", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=markup,
                              parse_mode="Markdown")

    # 10. عرض قائمة دورات الفقه (أزرار)
    elif call.data == "sub_c_fiqh":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for code, name in course_shortcuts_fiqh.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=code))
        markup.add(types.InlineKeyboardButton("🔙 العودة للأصناف", callback_data="main_courses"))
        bot.edit_message_text("⚖️ **دورات الفقه المتاحة:**", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=markup,
                              parse_mode="Markdown")

    # 11. عرض قائمة الدورات العامة (أزرار)
    elif call.data == "sub_c_gen":
        markup = types.InlineKeyboardMarkup(row_width=1)
        for code, name in course_shortcuts_general.items():
            markup.add(types.InlineKeyboardButton(name, callback_data=code))
        markup.add(types.InlineKeyboardButton("🔙 العودة للأصناف", callback_data="main_courses"))
        bot.edit_message_text("🌍 **دورات عامة وتطويرية:**", 
                              call.message.chat.id, 
                              call.message.message_id, 
                              reply_markup=markup,
                              parse_mode="Markdown")

    # 12. معالجة الضغط على دورة معينة (إرسال الرابط)
    elif call.data.startswith("course_aqida_"):
        course_name = course_shortcuts_aqida[call.data]
        course_link = DATA["courses_aqida"][course_name]
        bot.send_message(call.message.chat.id, f"🔗 **{course_name}**\n\nرابط الدورة: {course_link}", parse_mode="Markdown")

    elif call.data.startswith("course_fiqh_"):
        course_name = course_shortcuts_fiqh[call.data]
        course_link = DATA["courses_fiqh"][course_name]
        bot.send_message(call.message.chat.id, f"🔗 **{course_name}**\n\nرابط الدورة: {course_link}", parse_mode="Markdown")

    elif call.data.startswith("course_gen_"):
        course_name = course_shortcuts_general[call.data]
        course_link = DATA["courses_general"][course_name]
        bot.send_message(call.message.chat.id, f"🔗 **{course_name}**\n\nرابط الدورة: {course_link}", parse_mode="Markdown")

    # 13. العودة للرئيسية
    elif call.data in ["back_to_main", "back_main"]:
        bot.edit_message_text(
            "اختر القسم الذي ترغب فيه:",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu()
        )

    else:
        print(f"[WARNING] Callback غير معروف: {call.data}")

# الحصول على file_id عند إرسال ملف إلى البوت
@bot.message_handler(content_types=['document', 'audio', 'voice'])
def get_file_id(message):
    if message.document:
        bot.reply_to(message, f"كود الـ PDF:\n`{message.document.file_id}`", parse_mode="Markdown")
    elif message.audio:
        bot.reply_to(message, f"كود الصوت:\n`{message.audio.file_id}`", parse_mode="Markdown")
    elif message.voice:
        bot.reply_to(message, f"كود التسجيل:\n`{message.voice.file_id}`", parse_mode="Markdown")

# ===========================================
# تشغيل البوت في خيط منفصل مع Flask
# ===========================================
def run_bot():
    print("✅ البوت يعمل...")
    bot.infinity_polling()

if __name__ == "__main__":
    # تشغيل البوت في خلفية (thread منفصل)
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    
    # تشغيل تطبيق Flask (لإبقاء PythonAnywhere نشطاً)
    # ... باقي الكود ...

if __name__ == "__main__":
    bot_thread = Thread(target=run_bot)
    bot_thread.start()
    app.run(host='0.0.0.0', port=8080)
