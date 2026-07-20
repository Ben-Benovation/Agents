# monday API — מתכון לריצה אוטומטית (headless)

**למה זה קיים:** סשן מתוזמן/אוטומטי (Routine, fresh session) **לא נושא קונקטורי MCP** — אין בו `mcp__monday_com__*`. לכן ריצות אלידע האוטומטיות עובדות מול monday דרך ה-**REST/GraphQL API** עם טוקן, לא דרך ה-MCP. (בסשן אינטראקטיבי אפשר עדיין להשתמש ב-MCP.) כל הקריאות למטה **נבדקו ואומתו** ב-2026-07-20.

## גישה
- Endpoint: `https://api.monday.com/v2` · Header: `Authorization: $MONDAY_API_TOKEN` · Header: `API-Version: 2025-10`.
- העלאת קבצים: `https://api.monday.com/v2/file` (multipart).
- הטוקן במשתנה סביבה `MONDAY_API_TOKEN` (לא ב-git). דורש שמדיניות הרשת של הסביבה תתיר `api.monday.com` (Custom/Full).
- כל curl עם `--cacert /root/.ccr/ca-bundle.crt`.

## הקריאות (מאומתות ✅)
**זהות:** `{ me { id name account { id } } }` → user 62725549, account eliya.bnr.

**קריאת לוח המקורות (5100686191):**
```graphql
{ boards(ids: 5100686191){ items_page(limit: 50){ items { id name column_values(ids:["link_mm5ehn8n","color_mm5eh5sk","color_mm5et69k"]){ id text } } } } }
```

**דדופ — קריאת לוח היעד (5100685502):** אותו דפוס, בדוק שמות פריטים קיימים לפני יצירה.

**יצירת פריט + ערכי עמודות:**
```graphql
mutation ($board: ID!, $group: String!, $name: String!, $cv: JSON!) {
  create_item(board_id:$board, group_id:$group, item_name:$name, column_values:$cv){ id }
}
```
`column_values` = מחרוזת JSON: `color_mm5e3dsk={"label":"AI"}` · `color_mm5esd7d={"label":"שלישי"}` · `date_mm5e42n8={"date":"2026-07-21"}` · `link_mm5ed2rj={"url":"...","text":"..."}` · `numeric_mm5ept70="4"` · `date_mm5eg3r1={"date":"2026-07-20"}`. השאר `color_mm5e7nhy` (החלטת בן) ריק. group_id = `topics`.

**Doc בעמודת doc_mm5ekrf2 + תוכן:**
```graphql
mutation ($item: ID!, $col: String!){ create_doc(location:{board:{item_id:$item, column_id:$col}}){ id } }
```
ואז (⚠️ דורש API-Version **2025-10** — לא זמין בגרסאות ישנות):
```graphql
mutation ($docId: ID!, $md: String!){ add_content_to_doc_from_markdown(docId:$docId, markdown:$md){ success } }
```
ה-markdown = הפוסט כולו בתוך בלוק קוד (```) — משמר כוכביות להעתקה נקייה לוואטסאפ.

**העלאת תמונה לעמודת file_mm5ex900 (multipart):**
```bash
curl https://api.monday.com/v2/file -H "Authorization: $MONDAY_API_TOKEN" -H "API-Version: 2025-10" \
  -F 'query=mutation ($file: File!){ add_file_to_column(item_id: <ID>, column_id: "file_mm5ex900", file: $file){ id } }' \
  -F 'variables[file]=@image.png'
```

**התראה לבן:**
```graphql
mutation ($u: ID!, $t: ID!, $text: String!){ create_notification(user_id:$u, target_id:$t, text:$text, target_type:Project){ id } }
```
(user_id=62725549, target_id=פריט/לוח. מחזיר id "-1" — תקין.)

**מחיקת פריט (לניקוי בדיקות):** `mutation ($id: ID!){ delete_item(item_id:$id){ id } }`

## הערה על ה-Routine
ה-Routine `trig_01TyR5iw48Uv9cjSwj2aJhAS` מכיל פרומפט **עצמאי לגמרי** עם המתכון הזה בתוכו — הוא לא תלוי בקבצי הריפו (שממילא לא על main). לעריכת הפרומפט: מחיקה+יצירה מחדש של הטריגר (update_trigger לא משנה prompt).
