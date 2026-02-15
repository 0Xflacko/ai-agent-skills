# Omni-Video (O1)

- Route: `/global/dev/document-api/apiReference/model/OmniVideo`
- Source markdown path: `/src/docs/apiReference/model/OmniVideo/en.md`
- Source chunk: `https://s16-kling.klingai.com/kos/s101/nlav112918/api-doc/assets/en-BCCh840o.js`

## API Endpoints Referenced

- `create-omni-video`
- `query-omni-video`
- `query-omni-video-list`

## Extracted String Literals

```text
curl --location 'https://api-singapore.klingai.com/v1/videos/omni-video' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "kling-video-o1",
    "prompt": "<<<image_1>>> strolling through the streets of Tokyo, encountered <<<element_1>>> and <<<element_2>>>, and jumped into the arms of <<<element_2>>>. The video style matches that of <<<image_2>>>",
    "image_list": [
        {
        	"image_url": "xxxxx"
        },
        {
        	"image_url": "xxxxx"
        }
    ],
    "element_list": [
        {
        	"element_id": long
        },
        {
        	"element_id": long
        }
    ],
    "mode": "pro",
    "aspect_ratio": "1:1",
    "duration": "7"
}'
curl --location 'https://api-singapore.klingai.com/v1/videos/omni-video' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "kling-video-o1",
    "prompt": "Put the crown from <<<image_1>>> on the girl in blue from <<<video_1>>>.",
    "image_list": [
      {
      	"image_url": "xxx"
      }
    ],
    "video_list": [
      {
        "video_url":"xxxxxxxx",
        "refer_type":"base",
        "keep_original_sound":"yes"
      }
    ],
    "mode": "pro"
}'
curl --location 'https://api-singapore.klingai.com/v1/videos/omni-video' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "kling-video-o1",
    "prompt": "Referring to the camera movement style in <<<video_1>>>, generate a video: <<<element_1>>> and <<<element_2>>> strolling through the streets of Tokyo, encountering <<<image_1>>> by chance.",
    "image_list": [
      {
      	"image_url": "xxx"
      }
    ],
    "element_list": [
      {
      	"element_id": long
      },
      {
      	"element_id": long
      }
    ],
    "video_list": [
      {
        "video_url":"xxxxxxxx",
        "refer_type":"feature",
        "keep_original_sound":"yes"
      }
    ],
    "mode": "pro",
    "aspect_ratio": "1:1",
    "duration": "7"
}'
curl --location 'https://api-singapore.klingai.com/v1/videos/omni-video' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "kling-video-o1",
    "prompt": "Based on <<<video_1>>>, generate the next shot.",
    "video_list": [
      {
        "video_url":"xxxxxxxx",
        "refer_type":"feature",
        "keep_original_sound":"yes"
      }
    ],
    "mode": "pro"
}'
curl --location 'https://api-singapore.klingai.com/v1/videos/omni-video' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "kling-video-o1",
    "prompt": "The person in the video is dancing.",
    "image_list": [
      {
      	"image_url": "xxx",
        "type": "first_frame"
      },
      {
      	"image_url": "xxx",
        "type": "end_frame"
      }
    ],
    "mode": "pro"
}'
curl --location 'https://api-singapore.klingai.com/v1/videos/omni-video' \
--header 'Authorization: Bearer <token>' \
--header 'Content-Type: application/json' \
--data '{
    "model_name": "kling-video-o1",
    "prompt": "The person in the video is dancing.",
    "mode": "pro",
    "aspect_ratio": "1:1",
    "duration": "7"
}'
<h2 id="faq" tabindex="-1">FAQ</h2><p>1、 <strong>Video Duration Support</strong></p><ul><li><strong>Text-to-video and image-to-video (NOT including first/last frame)</strong>: Optional duration of 3~10s.</li><li><strong>When video input is provided (video_list is not empty) and video editing functionality (type = base) is used</strong>: Duration cannot be specified and will align with the input video.</li><li><strong>Other cases (when no video is provided but an image + subject is used for video generation, or when a video is provided with video type = feature)</strong>: Optional duration of 3-10s.</li></ul><p>2、 <strong>How to Extend a Video?</strong></p><ul><li>This can be achieved via “video reference”.</li><li>By inputting a video and using a prompt to direct the model to “generate the next shot” or “generate the previous shot”.</li></ul>
omni-video-(o1)
Omni-Video (O1)
Scenario invocation examples
The following is an example of scene code. For more effects and prompt words, please refer to: 
https://docs.qingque.cn/d/home/eZQDkhg4h2Qg8SEVSUTBdzYeY?identityId=2E1MlYrrPk4#section=h.8dg2lmxa6c5
noopener noreferrer
Kling Omni Model Example
image%2Felement-reference
Image/Element Reference
：Supports reference images/elements, including characters, items, backgrounds, and more, to generate with more creativity and consistency.
<<<image_1>>> strolling through the streets of Tokyo, encountered <<<element_1>>> and <<<element_2>>>, and jumped into the arms of <<<element_2>>>. The video style matches that of <<<image_2>>>
Input-based Modification
: Supports Inpainting/outpainting, or changing shot compositions or angles. It also supports localized or full-scale adjustments, such as modifying/swapping subjects, backgrounds, partial areas, styles, colors, weather, and more.
Put the crown from <<<image_1>>> on the girl in blue from <<<video_1>>>.
Video Reference
: Supports using reference video content to generate previous or next shots within the same context or set. It can also reference video actions or camera movements for generation.
Referring to the camera movement style in <<<video_1>>>, generate a video: <<<element_1>>> and <<<element_2>>> strolling through the streets of Tokyo, encountering <<<image_1>>> by chance.
Based on <<<video_1>>>, generate the next shot.
start-%26-end-frames
Start & End Frames
The person in the video is dancing.
Text To Video
Aspect Ratio Support
Not Supported
: Instruction-based transformation (video editing), image-to-video (not including first/last frame).
: Text-to-video, image/subject reference, video reference (other scenarios), video reference (generating next/previous shot).
```

## Raw Chunk Source

```javascript
import{_ as e}from"./ApiCodePanel-CIuPLAIK.js";import{_ as n}from"./OpenApi-CJm2vN96.js";import{a as o,k as i,b as t,f as a,ar as r,Y as l}from"./index-CyGZTn5T.js";import"./Index-Bsdwq5mu.js";import"./theme-AwbNpswb.js";import"./index-DutzOzEp.js";const d={class:"markdown-body"},s={__name:"en",setup:(s,{expose:p})=>(p({frontmatter:{}}),(s,p)=>{const m=n,c=e;return i(),o("div",d,[p[0]||(p[0]=t("h1",{id:"omni-video-(o1)",tabindex:"-1"},"Omni-Video (O1)",-1)),p[1]||(p[1]=t("hr",null,null,-1)),a(m,{endpoint:"create-omni-video"}),p[2]||(p[2]=t("hr",null,null,-1)),p[3]||(p[3]=t("h2",{id:"scenario-invocation-examples",tabindex:"-1"},"Scenario invocation examples",-1)),p[4]||(p[4]=t("blockquote",null,[t("p",null,[l("The following is an example of scene code. For more effects and prompt words, please refer to: "),t("a",{href:"https://docs.qingque.cn/d/home/eZQDkhg4h2Qg8SEVSUTBdzYeY?identityId=2E1MlYrrPk4#section=h.8dg2lmxa6c5",target:"_blank",rel:"noopener noreferrer"},"Kling Omni Model Example")])],-1)),p[5]||(p[5]=t("h3",{id:"image%2Felement-reference",tabindex:"-1"},"Image/Element Reference",-1)),p[6]||(p[6]=t("ul",null,[t("li",null,[t("strong",null,"Image/Element Reference"),l("：Supports reference images/elements, including characters, items, backgrounds, and more, to generate with more creativity and consistency.")])],-1)),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "<<<image_1>>> strolling through the streets of Tokyo, encountered <<<element_1>>> and <<<element_2>>>, and jumped into the arms of <<<element_2>>>. The video style matches that of <<<image_2>>>",\n    "image_list": [\n        {\n        \t"image_url": "xxxxx"\n        },\n        {\n        \t"image_url": "xxxxx"\n        }\n    ],\n    "element_list": [\n        {\n        \t"element_id": long\n        },\n        {\n        \t"element_id": long\n        }\n    ],\n    "mode": "pro",\n    "aspect_ratio": "1:1",\n    "duration": "7"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),p[7]||(p[7]=t("h3",{id:"transformation",tabindex:"-1"},"Transformation",-1)),p[8]||(p[8]=t("ul",null,[t("li",null,[t("strong",null,"Input-based Modification"),l(": Supports Inpainting/outpainting, or changing shot compositions or angles. It also supports localized or full-scale adjustments, such as modifying/swapping subjects, backgrounds, partial areas, styles, colors, weather, and more.")])],-1)),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "Put the crown from <<<image_1>>> on the girl in blue from <<<video_1>>>.",\n    "image_list": [\n      {\n      \t"image_url": "xxx"\n      }\n    ],\n    "video_list": [\n      {\n        "video_url":"xxxxxxxx",\n        "refer_type":"base",\n        "keep_original_sound":"yes"\n      }\n    ],\n    "mode": "pro"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),p[9]||(p[9]=t("h3",{id:"video-reference",tabindex:"-1"},"Video Reference",-1)),p[10]||(p[10]=t("ul",null,[t("li",null,[t("strong",null,"Video Reference"),l(": Supports using reference video content to generate previous or next shots within the same context or set. It can also reference video actions or camera movements for generation.")])],-1)),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "Referring to the camera movement style in <<<video_1>>>, generate a video: <<<element_1>>> and <<<element_2>>> strolling through the streets of Tokyo, encountering <<<image_1>>> by chance.",\n    "image_list": [\n      {\n      \t"image_url": "xxx"\n      }\n    ],\n    "element_list": [\n      {\n      \t"element_id": long\n      },\n      {\n      \t"element_id": long\n      }\n    ],\n    "video_list": [\n      {\n        "video_url":"xxxxxxxx",\n        "refer_type":"feature",\n        "keep_original_sound":"yes"\n      }\n    ],\n    "mode": "pro",\n    "aspect_ratio": "1:1",\n    "duration": "7"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "Based on <<<video_1>>>, generate the next shot.",\n    "video_list": [\n      {\n        "video_url":"xxxxxxxx",\n        "refer_type":"feature",\n        "keep_original_sound":"yes"\n      }\n    ],\n    "mode": "pro"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),p[11]||(p[11]=t("h3",{id:"start-%26-end-frames",tabindex:"-1"},"Start & End Frames",-1)),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "The person in the video is dancing.",\n    "image_list": [\n      {\n      \t"image_url": "xxx",\n        "type": "first_frame"\n      },\n      {\n      \t"image_url": "xxx",\n        "type": "end_frame"\n      }\n    ],\n    "mode": "pro"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),p[12]||(p[12]=t("h3",{id:"text-to-video",tabindex:"-1"},"Text To Video",-1)),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "The person in the video is dancing.",\n    "mode": "pro",\n    "aspect_ratio": "1:1",\n    "duration": "7"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),p[13]||(p[13]=r('<h2 id="faq" tabindex="-1">FAQ</h2><p>1、 <strong>Video Duration Support</strong></p><ul><li><strong>Text-to-video and image-to-video (NOT including first/last frame)</strong>: Optional duration of 3~10s.</li><li><strong>When video input is provided (video_list is not empty) and video editing functionality (type = base) is used</strong>: Duration cannot be specified and will align with the input video.</li><li><strong>Other cases (when no video is provided but an image + subject is used for video generation, or when a video is provided with video type = feature)</strong>: Optional duration of 3-10s.</li></ul><p>2、 <strong>How to Extend a Video?</strong></p><ul><li>This can be achieved via “video reference”.</li><li>By inputting a video and using a prompt to direct the model to “generate the next shot” or “generate the previous shot”.</li></ul>',5)),a(c,{"code-examples":[{language:"cURL",code:'curl --location \'https://api-singapore.klingai.com/v1/videos/omni-video\' \\\n--header \'Authorization: Bearer <token>\' \\\n--header \'Content-Type: application/json\' \\\n--data \'{\n    "model_name": "kling-video-o1",\n    "prompt": "Based on <<<video_1>>>, generate the next shot.",\n    "video_list": [\n      {\n        "video_url":"xxxxxxxx",\n        "refer_type":"feature",\n        "keep_original_sound":"yes"\n      }\n    ],\n    "mode": "pro"\n}\''}],"max-code-height":"none",class:"md-code-group-panel"}),p[14]||(p[14]=t("p",null,[l("3、 "),t("strong",null,"Aspect Ratio Support")],-1)),p[15]||(p[15]=t("ul",null,[t("li",null,[t("strong",null,"Not Supported"),l(": Instruction-based transformation (video editing), image-to-video (not including first/last frame).")]),t("li",null,[t("strong",null,"Supported"),l(": Text-to-video, image/subject reference, video reference (other scenarios), video reference (generating next/previous shot).")])],-1)),p[16]||(p[16]=t("hr",null,null,-1)),a(m,{endpoint:"query-omni-video"}),p[17]||(p[17]=t("hr",null,null,-1)),a(m,{endpoint:"query-omni-video-list"})])})};export{s as default};
//# sourceMappingURL=en-BCCh840o.js.map

```
