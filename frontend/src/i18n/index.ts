import i18n from 'i18next'
import { initReactI18next } from 'react-i18next'
import en from './locales/en/invoice.json'
import hi from './locales/hi/invoice.json'

i18n.use(initReactI18next).init({
  resources: { en: { invoice: en }, hi: { invoice: hi } },
  lng: 'en',
  fallbackLng: 'en',
  interpolation: { escapeValue: false }
})
export default i18n
