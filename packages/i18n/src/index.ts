/**
 * Shared i18n module for CourseLit packages.
 *
 * Locale is selected via NEXT_PUBLIC_LOCALE env var (default: "en").
 * All packages in the monorepo can import from "@courselit/i18n".
 *
 * To add a new language:
 *   1. Create src/messages/<locale>/messages.json
 *   2. Add the import and entry to the `locales` map below
 */

import en from "./messages/en/messages.json";
import ptBR from "./messages/pt-BR/messages.json";

type Messages = typeof en;

const locales: Record<string, Messages> = {
    en,
    "pt-BR": ptBR,
};

const locale = process.env.NEXT_PUBLIC_LOCALE || "en";

export const messages: Messages = locales[locale] || locales.en;
export const currentLocale = locale;
export type { Messages };
