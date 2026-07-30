# monday API — מתכון לריצה אוטומטית (headless)

**למה זה קיים:** סשן מתוזמן (Routine, fresh session) **לא נושא קונקטורי MCP** — אין בו `mcp__monday_com__*`. לכן ריצות הרדאר האוטומטיות עובדות מול monday דרך ה-**REST/GraphQL API** עם טוקן, לא דרך MCP. (בסשן אינטראקטיבי אפשר עדיין להשתמש ב-MCP.) **כל הקריאות למטה נבדקו ואומתו מקצה-לקצה על בורד `5101310265` ב-2026-07-30.**

## גישה
- Endpoint: `https://api.monday.com/v2` · Headers: `Authorization: $MONDAY_API_TOKEN` · `API-Version: 2025-10` · `Content-Type: application/json`.
- הטוקן במשתנה סביבה `MONDAY_API_TOKEN` (לא ב-git). דורש שמדיניות הרשת תתיר `api.monday.com`.
- כל curl עם `--cacert /root/.ccr/ca-bundle.crt`.

## מזהים
board `5101310265` · group "השבוע" `group_mm5rsesk` · group "ארכיון" `group_mm5rhdb8` · user בן `62725549`.

## עמודות (column_id → פורמט ערך)
| column_id | כותרת | פורמט ב-`column_values` (JSON) |
| --- | --- | --- |
| `link_mm5rvtkx` | קישור למקור | `{"url":"https://...","text":"כותרת המקור"}` |
| `color_mm5rscgs` | מקור | `{"label":"GitHub"}` (Anthropic/GitHub/Hacker News/Reddit/Make/monday) |
| `numeric_mm5rm4pc` | באזז | `"4"` |
| `numeric_mm5rjj53` | הדגמה | `"5"` |
| `numeric_mm5rwc2y` | פער עברית | `"4"` |
| `numeric_mm5rfwab` | רלוונטיות עסקית | `"3"` |
| `numeric_mm5r1erj` | ציון כולל | `"16"` (הסכום — הרוטינה מחשבת) |
| `long_text_mm5ra6ew` | זווית לסרטון | `{"text":"משפט אחד..."}` |
| `long_text_mm5r2zyz` | מה להדגים | `{"text":"• בולט 1\n• בולט 2\n• בולט 3"}` |
| `color_mm5r8skp` | סטטוס | `{"label":"חדש"}` |
| `date_mm5rz82n` | תאריך איתור | `{"date":"2026-08-02"}` |

## הקריאות (מאומתות ✅)

**זהות:** `{ me { id name account { id } } }`

**דדופ — קריאת קישורי הבורד (לפני כל יצירה):**
```graphql
{ boards(ids:5101310265){ items_page(limit:200){ items { id name column_values(ids:["link_mm5rvtkx"]){ id text } } } } }
```
⚠️ עמודת link מחזירה ב-`text` את **"הכותרת - ה-URL"** (למשל `"פריט בדיקה - https://example.com/validation"`). לכן דדופ = בדוק אם ה-URL של המועמד מופיע כתת-מחרוזת באחד מ-`text` הקיימים. דלג אם קיים.

**יצירת פריט + כל ערכי העמודות:**
```graphql
mutation($b:ID!,$g:String!,$n:String!,$cv:JSON!){
  create_item(board_id:$b, group_id:$g, item_name:$n, column_values:$cv){ id }
}
```
`column_values` = מחרוזת JSON עם ה-column_ids מהטבלה למעלה. `group_id`=`group_mm5rsesk`. תוויות הסטטוס (`מקור`, `סטטוס`) כבר מוגדרות מראש בבורד — אין צורך ב-create_labels_if_missing; אם בכל זאת תוסיפו ערך חדש, הוסיפו את הארגומנט `create_labels_if_missing:true`.

**מחיקת פריט (לניקוי בדיקות):**
```graphql
mutation($id:ID!){ delete_item(item_id:$id){ id } }
```

**התראה לבן (אופציונלי בסיום ריצה):**
```graphql
mutation($u:ID!,$t:ID!,$text:String!){ create_notification(user_id:$u, target_id:$t, text:$text, target_type:Project){ id } }
```
(user_id=62725549, target_id=board/item.)

## דוגמת Python מינימלית (urllib, ללא תלויות)
```python
import json, os, ssl, urllib.request
ctx = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
def gql(q, v=None):
    body = json.dumps({"query": q, "variables": v or {}}).encode("utf-8")
    req = urllib.request.Request("https://api.monday.com/v2", data=body, headers={
        "Authorization": os.environ["MONDAY_API_TOKEN"], "API-Version": "2025-10",
        "Content-Type": "application/json"})
    out = json.loads(urllib.request.urlopen(req, context=ctx, timeout=60).read())
    if "errors" in out: raise RuntimeError(json.dumps(out["errors"], ensure_ascii=False))
    return out["data"]
```
