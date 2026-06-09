import streamlit as st
from core.driver_factory import DriverFactory
from tests.test_login import test_login

st.set_page_config(page_title="Self-Healing Selenium", page_icon="🔧")
st.title("🔧 Self-Healing Selenium Framework")
st.markdown("**Target:** OrangeHRM Demo Login Page")
st.divider()

if st.button("▶️ Run Test Now", type="primary"):
    with st.spinner("Running Selenium test..."):
        log = st.empty()
        messages = []

        def log_msg(msg):
            messages.append(msg)
            log.markdown("\n\n".join(messages))

        driver = DriverFactory.get_driver()
        try:
            log_msg("🌐 Opening OrangeHRM login page...")
            log_msg("🔄 Running self-healing login test...")
            test_login(driver)
            log_msg("✅ All tests passed!")
            st.success("✅ Login Test PASSED")
            st.balloons()

        except AssertionError as e:
            log_msg(f"❌ TEST FAILED: {e}")
            st.error(f"❌ Test Failed: {e}")

        except Exception as e:
            log_msg(f"❌ UNEXPECTED ERROR: {e}")
            st.error(f"❌ Unexpected Error: {e}")

        finally:
            driver.quit()
            log_msg("🔒 Browser closed.")