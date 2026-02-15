# dialog/0126

- Route: `/global/dev/document-api/dialog/0126`
- Source markdown path: `/src/docs/dialog/0126/en.md`
- Source chunk: `https://s16-kling.klingai.com/kos/s101/nlav112918/api-doc/assets/en-Dd1hnxOb.js`

## Extracted String Literals

```text
{
  "code": 0,
  "message": "string",
  "request_id": "string",
  "data": {
    "task_id": "string",
    "task_status": "string",
    "task_status_msg": "string",
    "task_info": {
      "external_task_id": "string"
    },
    "task_result": {
      "videos": [
        {
          "id": "string",
          "url": "string",
          "watermark_url": "string", // NEW: URL for generating videos, hotlink protection format.
          "duration": "string"
        }
      ]
    },
    "watermark_info": { // NEW
      "enabled": boolean // NEW
    },
    "final_unit_deduction": "5",  // NEW: task unit deduction results.
    "created_at": 1722769557708,
    "updated_at": 1722769557708
  }
}
Dear Developers,
To improve the usability of our API, we are introducing task unit deduction results in the API response. Additionally, the option to generate videos or images with watermarks will now be supported. You can access these updates via the final_unit_deduction and watermark_url fields, which will be available at 18:00 on January 23, 2026 (UTC+8). Please ensure that your current JSON parsing solution is compatible with these changes.
Reference materials:
Should you have any questions, please don’t hesitate to contact us via the support ticket system.
Thank you for your continued support of Kling AI.
```

## Raw Chunk Source

```javascript
import{_ as e}from"./ApiCodePanel-CIuPLAIK.js";import{a as n,k as t,b as s,f as a}from"./index-CyGZTn5T.js";import"./Index-Bsdwq5mu.js";import"./theme-AwbNpswb.js";import"./index-DutzOzEp.js";const i={class:"markdown-body"},o={class:"container"},r={__name:"en",setup:(r,{expose:l})=>(l({frontmatter:{}}),(r,l)=>{const u=e;return t(),n("div",i,[l[1]||(l[1]=s("p",null,"Dear Developers,",-1)),l[2]||(l[2]=s("p",null,"To improve the usability of our API, we are introducing task unit deduction results in the API response. Additionally, the option to generate videos or images with watermarks will now be supported. You can access these updates via the final_unit_deduction and watermark_url fields, which will be available at 18:00 on January 23, 2026 (UTC+8). Please ensure that your current JSON parsing solution is compatible with these changes.",-1)),s("div",o,[l[0]||(l[0]=s("ul",null,[s("li",null,[s("strong",null,"Reference materials:")])],-1)),a(u,{"code-examples":[{language:"JSON",code:'{\n  "code": 0,\n  "message": "string",\n  "request_id": "string",\n  "data": {\n    "task_id": "string",\n    "task_status": "string",\n    "task_status_msg": "string",\n    "task_info": {\n      "external_task_id": "string"\n    },\n    "task_result": {\n      "videos": [\n        {\n          "id": "string",\n          "url": "string",\n          "watermark_url": "string", // NEW: URL for generating videos, hotlink protection format.\n          "duration": "string"\n        }\n      ]\n    },\n    "watermark_info": { // NEW\n      "enabled": boolean // NEW\n    },\n    "final_unit_deduction": "5",  // NEW: task unit deduction results.\n    "created_at": 1722769557708,\n    "updated_at": 1722769557708\n  }\n}'}],"show-header":!1,"max-code-height":"none",class:"md-code-group-panel"})]),l[3]||(l[3]=s("p",null,"Should you have any questions, please don’t hesitate to contact us via the support ticket system.",-1)),l[4]||(l[4]=s("p",null,"Thank you for your continued support of Kling AI.",-1))])})};export{r as default};
//# sourceMappingURL=en-Dd1hnxOb.js.map

```
