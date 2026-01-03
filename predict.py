import streamlit as st
import pickle
import pandas as pd


# سازگاری با Streamlit قدیمی (برای جلوگیری از AttributeError)
if not hasattr(st, "divider"):
    def _divider():
        st.markdown("---")
    st.divider = _divider


@st.cache_resource
def load_model():
    return pickle.load(open("model.pkl", "rb"))


def b2i(s: str) -> int:
    return 1 if s == "بله" else 0


def probability_gauge(p: float):
    """
    نمایش حرفه‌ای‌تر احتمال: هم Progress هم متن رنگی/ایموجی
    """
    p = max(0.0, min(1.0, p))
    percent = int(round(p * 100))

    st.markdown('<div class="gauge-wrap">', unsafe_allow_html=True)
    st.markdown(f"**📊 احتمال تقلب:** {percent}%")
    st.progress(percent)

    if percent >= 80:
        st.error("سطح ریسک: خیلی بالا 🚨")
    elif percent >= 60:
        st.warning("سطح ریسک: بالا ⚠️")
    elif percent >= 45:
        st.info("سطح ریسک: نزدیک مرز تصمیم 🟡")
    else:
        st.success("سطح ریسک: پایین ✅")
    st.markdown('</div>', unsafe_allow_html=True)


def set_preset(name: str):
    """
    دو سناریوی آماده: یکی سالم، یکی مشکوک
    مقادیر نمونه‌اند و فقط برای دمو و تجربه کاربری هستند.
    """
    if name == "سناریوی سالم ✅":
        st.session_state.update({
            "distance_from_home": 1.2,
            "distance_from_last_transaction": 0.8,
            "ratio_to_median_purchase_price": 1.0,
            "repeat_retailer": "بله",
            "used_chip": "بله",
            "used_pin_number": "بله",
            "online_order": "خیر",
        })
    else:  # مشکوک
        st.session_state.update({
            "distance_from_home": 120.0,
            "distance_from_last_transaction": 95.0,
            "ratio_to_median_purchase_price": 6.5,
            "repeat_retailer": "خیر",
            "used_chip": "خیر",
            "used_pin_number": "خیر",
            "online_order": "بله",
        })


def predict_page():
    model = load_model()

    st.markdown("""
    <div class="card">
      <h3>🔎 پیش‌بینی تراکنش</h3>
      <div class="muted">مقادیر را وارد کنید یا از سناریوی آماده استفاده کنید، سپس «پیش‌بینی» را بزنید.</div>
    </div>
    """, unsafe_allow_html=True)

    # Presets
    pcol1, pcol2, pcol3 = st.columns([1.2, 1.2, 2])
    with pcol1:
        if st.button("سناریوی سالم ✅", use_container_width=True):
            set_preset("سناریوی سالم ✅")
    with pcol2:
        if st.button("سناریوی مشکوک 🚨", use_container_width=True):
            set_preset("سناریوی مشکوک 🚨")
    with pcol3:
        st.caption("سناریوها فقط برای تست و دمو هستند (اعداد نمونه‌اند).")

    st.markdown("---")

    # Defaults in session_state (so presets can fill them)
    defaults = {
        "distance_from_home": 1.0,
        "distance_from_last_transaction": 1.0,
        "ratio_to_median_purchase_price": 1.0,
        "repeat_retailer": "بله",
        "used_chip": "بله",
        "used_pin_number": "بله",
        "online_order": "خیر",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

    with st.form("fraud_form"):
        c1, c2 = st.columns(2)

        with c1:
            st.subheader("📍 مقادیر عددی")
            distance_from_home = st.number_input(
                "فاصله از خانه (km)",
                min_value=0.0, step=0.1,
                value=float(st.session_state["distance_from_home"]),
                key="distance_from_home"
            )
            distance_from_last_transaction = st.number_input(
                "فاصله از تراکنش قبلی (km)",
                min_value=0.0, step=0.1,
                value=float(st.session_state["distance_from_last_transaction"]),
                key="distance_from_last_transaction"
            )
            ratio_to_median_purchase_price = st.number_input(
                "نسبت مبلغ به میانه خریدها",
                min_value=0.0, step=0.1,
                value=float(st.session_state["ratio_to_median_purchase_price"]),
                key="ratio_to_median_purchase_price"
            )

        with c2:
            st.subheader("🧾 رفتار تراکنش")
            repeat_retailer = st.radio("خرید تکراری از همین فروشنده", ["خیر", "بله"], horizontal=True, key="repeat_retailer")
            used_chip = st.radio("استفاده از چیپ کارت", ["خیر", "بله"], horizontal=True, key="used_chip")
            used_pin_number = st.radio("استفاده از PIN", ["خیر", "بله"], horizontal=True, key="used_pin_number")
            online_order = st.radio("سفارش آنلاین", ["خیر", "بله"], horizontal=True, key="online_order")

        submitted = st.form_submit_button("🔮 پیش‌بینی", use_container_width=True)

    # Build input for model (order must match training columns)
    input_dict = {
        "distance_from_home": float(distance_from_home),
        "distance_from_last_transaction": float(distance_from_last_transaction),
        "ratio_to_median_purchase_price": float(ratio_to_median_purchase_price),
        "repeat_retailer": b2i(repeat_retailer),
        "used_chip": b2i(used_chip),
        "used_pin_number": b2i(used_pin_number),
        "online_order": b2i(online_order),
    }
    input_df = pd.DataFrame([input_dict])

    with st.expander("👀 خلاصه ورودی‌ها"):
        st.dataframe(input_df, use_container_width=True)

    if submitted:
        # Simple sanity check
        if input_dict["distance_from_home"] == 0 and input_dict["distance_from_last_transaction"] == 0 and input_dict["ratio_to_median_purchase_price"] == 0:
            st.warning("سه مقدار عددی صفر است؛ اگر مطمئن نیستید، مقادیر واقعی‌تری وارد کنید.")

        pred = int(model.predict(input_df)[0])

        st.markdown("---")

        # Show result
        if pred == 1:
            st.error("🚨 نتیجه: تراکنش **مشکوک/تقلبی** تشخیص داده شد.")
        else:
            st.success("✅ نتیجه: تراکنش **سالم** تشخیص داده شد.")

        # Probability if available
        if hasattr(model, "predict_proba"):
            proba_fraud = float(model.predict_proba(input_df)[0][1])
            probability_gauge(proba_fraud)
        else:
            st.info("این مدل خروجی احتمال (predict_proba) ندارد؛ فقط نتیجه 0/1 نمایش داده شد.")
