/**
 * CIANDLITHE wholesale-copy of cianfhoghlaim/cianfhoghlaim @ main branch.
 *
 * Original: cianfhoghlaim/cianfhoghlaim (per the openspec/changes/ciandlithe-repo-bootstrap-v2/specs/ciandlithe-bootstrap-v2/spec.md).
 * Migrated to ciandlithe: 2026-08-23
 * Licence: BUSL-1.1 (per LICENSE.md)
 */
import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import commonEn from "./resources/common/en/common.json";
import commonGa from "./resources/common/ga/common.json";
import musicEn from "./resources/streams/music/en/persona.json";
import musicGa from "./resources/streams/music/ga/persona.json";
import teachingEn from "./resources/streams/teaching/en/persona.json";
import teachingGa from "./resources/streams/teaching/ga/persona.json";

const resources = {
  en: {
    common: commonEn,
    music: musicEn,
    teaching: teachingEn,
  },
  ga: {
    common: commonGa,
    music: musicGa,
    teaching: teachingGa,
  },
};

i18n.use(initReactI18next).init({
  resources,
  lng: "en",
  fallbackLng: "en",
  defaultNS: "common",
  interpolation: { escapeValue: false },
});

export default i18n;
