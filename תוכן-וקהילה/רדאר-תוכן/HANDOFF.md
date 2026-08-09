# Handoff — רדאר תוכן (Content Radar)

מסמך המשכיות. עודכן: 2026-07-30.

## מה זה
גיוס העובד הדיגיטלי **רדאר תוכן** — סורק בכל יום ראשון בבוקר את סביבת Claude/AI לאוטומציה מהשבוע האחרון, מדרג מועמדים לפי 4 קריטריונים, וכותב **עד 7 נושאים בציון כולל ≥ 13** כתור מדורג בבורד "רדאר תוכן". בן בוחר מהתור מה להפיק. אם אין נושא ששווה — לא כותב כלום.

## ריפו / Git
- ריפו: **Ben-Benovation/Agents** · ענף: **claude/content-radar-automation-0clj8t**.
- תיקיית הסוכן: `תוכן-וקהילה/רדאר-תוכן/` — `AGENT.md`, `ROLE-DOSSIER.md`, `selection-rubric.md`, `sources.json`, `monday-setup.md`, `monday-api-recipe.md`, `routine-prompt.md`, `HANDOFF.md`.
- סקילים גלובליים רלוונטיים: `agent-hiring` (עיצוב תיק), `whatsapp-updates`/`instagram-content` (הפקת התוכן בהמשך).

## החלטות שסוכמו עם בן (2026-07-30)
1. **ארכיטקטורה:** Routine שבועי + monday API (סשן טרי לא נושא MCP → כתיבה דרך טוקן).
2. **מקורות:** `sources.json` בריפו + מוטמע בפרומפט ה-Routine.
3. **שלבים ידניים:** אימות ביקוש (Trends/יוטיוב) ויצירת תסריט במעבר ל"בהפקה" — נשארים ידניים כרגע, מתועדים בתיק §7.
4. **סף ותפוקה:** ציון כולל ≥ 13, מקסימום 7/שבוע, ממוינים יורד. הרף גובר על מילוי מקום.
5. **הרצה ראשונה ידנית** לפני הפעלת התזמון.
6. **בורד נפרד מאלידע** (פלט שונה: תור נושאי וידאו מול טיוטות וואטסאפ), למרות חפיפת המקורות.

## monday.com
- חשבון: `eliyabnr-company` · משתמש בן: **62725549** · workspace **CRM** `2199900` · תיקייה **עדכוני קהילה** `3199324`.
- **בורד "רדאר תוכן"** `5101310265` — קבוצות: `group_mm5rsesk`=השבוע (כותבים לכאן), `group_mm5rhdb8`=ארכיון.
- עמודות: `link_mm5rvtkx`=קישור למקור · `color_mm5rscgs`=מקור · `numeric_mm5rm4pc`=באזז · `numeric_mm5rjj53`=הדגמה · `numeric_mm5rwc2y`=פער עברית · `numeric_mm5rfwab`=רלוונטיות עסקית · `numeric_mm5r1erj`=ציון כולל · `long_text_mm5ra6ew`=זווית לסרטון · `long_text_mm5r2zyz`=מה להדגים · `color_mm5r8skp`=סטטוס (חדש/בבדיקה/בהפקה/פורסם/נפסל) · `date_mm5rz82n`=תאריך איתור.
- **נבדק ואומת (2026-07-30):** בורד+עמודות+קבוצות+תוויות נוצרו דרך ה-API. נתיב headless מלא (create_item עם כל סוגי העמודות → dedupe read → delete_item) עבד מקצה-לקצה. הבורד **ריק** ומוכן לריצה הראשונה.

## סודות / סביבה
- `MONDAY_API_TOKEN` — **מוגדר כ-env ומאומת** (HTTP 200 מ-build env). לא ב-git.
- `GEMINI_API_KEY` — מוגדר (לא בשימוש כרגע; שמור לעתיד אם ירצו תמונות).
- כל curl עם `--cacert /root/.ccr/ca-bundle.crt`.

## ⚠️ חסם עיקרי — מדיניות רשת לסריקה
- **build env (הסביבה הזו) חוסמת את מקורות הסריקה** (proxy 403): `hn.algolia.com`, `reddit.com`, `developer.monday.com`, `make.com`, `www.anthropic.com`. נגישים ממנה רק `raw.githubusercontent.com` ו-`api.monday.com`. ה-GitHub API scoped לריפו המוגדר (search חסום).
- **המשמעות:** הכתיבה למאנדיי עובדת מכאן, אבל **הסריקה החיה לא יכולה לרוץ מסביבה זו.** הריצה הראשונה החיה + הריצות המתוזמנות צריכות סביבה עם **מדיניות רשת פתוחה** למארחי המקורות (Custom/Full + הוספת המארחים, כמו שנעשה לאלידע עם `api.monday.com`).
- **פעולה נדרשת מבן:** לוודא שסביבת ה-Routine פתוחה למארחים ברשימה למטה, ו-`MONDAY_API_TOKEN` מוגדר בה כ-env.

### allowlist מלא — כל המארחים (כולם HTTPS/443)
**קבוצה A — ליבה (חובה):**
| Host | למה | סטטוס בבנייה |
| --- | --- | --- |
| `api.monday.com` | כתיבה לבורד + dedupe | ✅ נגיש |
| `raw.githubusercontent.com` | Claude Code CHANGELOG | ✅ נגיש |
| `api.github.com` | ריפו בתאוצה + issues (ראה הערת GitHub) | ⚠️ מוגבל |

**קבוצה B — מקורות סריקה (שכבה 0–1):**
| Host | למה | סטטוס בבנייה |
| --- | --- | --- |
| `www.anthropic.com` | Anthropic News | ❌ חסום |
| `docs.claude.com` | Claude/API release notes | ❌ חסום |
| `docs.anthropic.com` | גיבוי release notes | ❌ חסום |
| `hn.algolia.com` | Hacker News API | ❌ חסום |
| `www.reddit.com` | Reddit (4 subs) | ❌ חסום |
| `www.make.com` | Make release notes | ❌ חסום |
| `developer.monday.com` | monday changelog | ❌ חסום |
| `api.npmjs.org` | npm download trends | ✅ בד"כ נגיש |

**קבוצה C — שכבה 2 (אופציונלי):**
| Host | למה | סטטוס בבנייה |
| --- | --- | --- |
| `github.com` | MCP registry (modelcontextprotocol/servers) | ❌ חסום |
| `simonwillison.net` | RSS | ❌ חסום |
| `www.latent.space` | RSS (Latent Space) | ❌ חסום |

⚠️ **הערת GitHub:** החסימה של `api.github.com` היא הגבלת Claude Code (הגישה scoped לריפו המוגדר), **לא** מדיניות הרשת — פתיחת רשת לבדה עשויה לא לפתוח חיפוש ריפואים רוחבי. fallback: curl ישיר ל-endpoint ציבורי או עמוד `github.com/trending`. לאמת בריצה הראשונה.
מינימום להפעלה: קבוצות A+B. קבוצה C משדרגת כיסוי; הרוטינה מדלגת בשקט על מה שחסום.

## תזמון — פעיל ✅
- **trigger_id:** `trig_01Ck8ZWmbf8Y7TcyB1Yjt2WG` · **enabled** · `create_new_session_on_fire=true`
- **cron:** `12 5 * * 0` (UTC) = יום ראשון 08:12 שעון ישראל (IDT). ריצה ראשונה מתוזמנת: 2026-08-16 05:12 UTC.
- **התראות:** push לנייד בסוף כל ריצה (email כבוי).
- **prompt:** self-contained (זהה ל-[`routine-prompt.md`](routine-prompt.md), עם רשימת המקורות שאומתו 2026-08-09).
- ⚠️ הטריגר **לא נושא קונקטורי MCP** (אזהרה צפויה) — הכתיבה למאנדיי דרך `MONDAY_API_TOKEN` (אומת).
- **להשהיה:** `update_trigger(trig_01Ck8ZWmbf8Y7TcyB1Yjt2WG, enabled:false)` או מרשימת ה-Routines. לעריכת הפרומפט: מחיקה+יצירה מחדש (`update_trigger` לא משנה prompt).

## ריצת אימות חיה (2026-08-09) ✅
בוצעה ריצה אמיתית מקצה-לקצה (סריקת HN + CHANGELOG + בלוגים → ניקוד → כתיבה). **7 פריטים אמיתיים נכתבו** לקבוצת "השבוע" (ציונים 18/18/17/17/17/17/15), dedupe נבדק (בורד היה ריק). הבורד מוכן לצפייה של בן.

## הצעד הבא המומלץ (לפי עדיפות)
1. בן פותח את מדיניות הרשת בסביבת ה-Routine למקורות הסריקה + מגדיר `MONDAY_API_TOKEN` שם.
2. ריצת אימות ידנית חיה (fire_trigger) → לבדוק שהתור מתמלא נכון ושה-dedupe עובד.
3. אם תקין → `update_trigger(enabled:true)` להפעלת התזמון השבועי.
4. אחרי ~4 ריצות → לולאת למידה ראשונה (רובריקה/מקורות).
