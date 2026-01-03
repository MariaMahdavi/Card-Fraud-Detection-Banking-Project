import streamlit as st
from predict import predict_page

def inject_css():
    st.markdown("""
    <style>
    /* --- RTL & Global --- */
    html, body, [class*="css"]  {
        direction: rtl;
        text-align: right;
        font-family: Vazirmatn, IRANSans, Arial, sans-serif;
    }

    /* Hide Streamlit default UI (optional) */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stToolbar"] {visibility: hidden;}

    /* --- App container spacing --- */
    .block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

    /* --- Hero --- */
    .hero {
        border-radius: 18px;
        padding: 18px 18px;
        background: linear-gradient(135deg, rgba(74,144,226,0.25), rgba(80,227,194,0.20));
        border: 1px solid rgba(0,0,0,0.06);
        margin-bottom: 14px;
    }
    .hero h1 { margin: 0; font-size: 1.6rem; }
    .hero p { margin: 6px 0 0 0; opacity: 0.85; }

    /* --- Cards --- */
    .card {
        border-radius: 16px;
        padding: 14px 14px;
        border: 1px solid rgba(0,0,0,0.08);
        background: rgba(255,255,255,0.65);
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
    }
    .card h3 { margin: 0 0 6px 0; font-size: 1.05rem; }
    .muted { opacity: 0.75; font-size: 0.95rem; }

    /* --- Badge --- */
    .badge {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        background: rgba(0,0,0,0.06);
        font-size: 0.9rem;
        margin-top: 6px;
    }

    /* --- Gauge container --- */
    .gauge-wrap {
        border-radius: 16px;
        padding: 12px 12px;
        border: 1px solid rgba(0,0,0,0.08);
        background: rgba(255,255,255,0.65);
        box-shadow: 0 6px 20px rgba(0,0,0,0.05);
        margin-top: 8px;
    }
    </style>
    """, unsafe_allow_html=True)


def about_page():
    st.markdown("""
    <div class="hero">
      <h1>ℹ️ درباره مدل</h1>
      <p>این صفحه خلاصه‌ای از مدل و منطق تصمیم‌گیری را نشان می‌دهد.</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div class="card">
          <h3>🤖 الگوریتم</h3>
          <div class="muted">Random Forest Classifier</div>
          <div class="badge">تصمیم‌گیری با رأی چندین درخت</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
          <h3>📈 عملکرد</h3>
          <div class="muted">طبق گزارش پروژه، دقت مدل حدود 99٪ است.</div>
          <div class="badge">ارزیابی روی داده تست</div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("این عدد مطابق توضیحات مستند پروژه است. :contentReference[oaicite:1]{index=1}")

    st.markdown("""
    <div class="card" style="margin-top:12px;">
      <h3>🧠 مدل چه ورودی‌هایی می‌گیرد؟</h3>
      <div class="muted">
        فاصله از خانه، فاصله از تراکنش قبلی، نسبت مبلغ به میانه خریدها،
        آنلاین بودن، استفاده از چیپ، استفاده از PIN، و تکراری بودن فروشنده.
      </div>
    </div>
    """, unsafe_allow_html=True)


def help_page():
    st.markdown("""
    <div class="hero">
      <h1>📘 راهنما</h1>
      <p>چطور از اپ استفاده کنیم و نتایج را چطور بخوانیم؟</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
      <h3>✅ مراحل استفاده</h3>
      <ol class="muted">
        <li>به صفحه «پیش‌بینی» برو.</li>
        <li>ویژگی‌های تراکنش را وارد کن (یا از سناریوهای آماده استفاده کن).</li>
        <li>روی دکمه «پیش‌بینی» بزن.</li>
        <li>نتیجه و «احتمال تقلب» را ببین.</li>
      </ol>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card" style="margin-top:12px;">
      <h3>🟡 تفسیر احتمال</h3>
      <div class="muted">
        اگر احتمال نزدیک 50٪ باشد، یعنی مدل بین دو حالت مردد است و در دنیای واقعی بهتر است بررسی دستی هم انجام شود.
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.info("این ابزار آموزشی است و جایگزین قوانین امنیتی و کنترل‌های بانکی واقعی نیست.")


def main():
    st.set_page_config(page_title="Fraud Guard", page_icon="💳", layout="wide")
    inject_css()

    # Hero top (logo optional)
    left, right = st.columns([1, 3])
    with left:
        try:
            st.image("assets/logo.png", use_container_width=True)
        except Exception:
            st.markdown("### 💳")

    with right:
        st.markdown("""
        <div class="hero">
          <h1>Fraud Guard — تشخیص تقلب تراکنش</h1>
          <p>یک وب‌اپ سبک برای پیش‌بینی «سالم/مشکوک» بودن تراکنش با مدل یادگیری ماشین.</p>
        </div>
        """, unsafe_allow_html=True)

    # Navigation
    page = st.sidebar.radio(
        "منو",
        ["پیش‌بینی", "راهنما", "درباره مدل"],
        index=0
    )

    if page == "پیش‌بینی":
        predict_page()
    elif page == "راهنما":
        help_page()
    else:
        about_page()


if __name__ == "__main__":
    main()
