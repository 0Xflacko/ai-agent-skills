# Video Effects

- Route: `/global/dev/document-api/apiReference/model/videoEffects`
- Source markdown path: `/src/docs/apiReference/model/videoEffects/en.md`
- Source chunk: `https://s16-kling.klingai.com/kos/s101/nlav112918/api-doc/assets/en-KpS5L_ZF.js`

## API Endpoints Referenced

- `create-video-effects`
- `query-video-effects-single`
- `query-video-effects-list`

## Extracted String Literals

```text
{
  "effect_scene": "pet_lion",
  "input":{
    "image":"https://p4-kling.klingai.com/bs2/upload-ylab-stunt/c54e463c95816d959602f1f2541c62b2.png?x-kcdn-pid=112452"
  }
}
{
  "effect_scene": "hug_pro",
  "input": {
    "images": [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg"
    ]
  }
}
Video Effects
Single-image Effect Request Example
Applicable to 216 single-image effects
https://p4-kling.klingai.com/bs2/upload-ylab-stunt/c54e463c95816d959602f1f2541c62b2.png?x-kcdn-pid=112452
Dual-character Effect Request Example
Applicable to 6 dual-character effects (snow_night_kiss, eternal_kiss, cheers_2026, fight_pro, hug_pro, heart_gesture_pro).
```

## Raw Chunk Source

```javascript
import{_ as e}from"./ApiCodePanel-CIuPLAIK.js";import{_ as n}from"./OpenApi-CJm2vN96.js";import{a as t,k as a,b as s,f as l}from"./index-CyGZTn5T.js";import"./Index-Bsdwq5mu.js";import"./theme-AwbNpswb.js";import"./index-DutzOzEp.js";const i={class:"markdown-body"},o={__name:"en",setup:(o,{expose:p})=>(p({frontmatter:{}}),(o,p)=>{const c=n,r=e;return a(),t("div",i,[p[0]||(p[0]=s("h1",{id:"video-effects",tabindex:"-1"},"Video Effects",-1)),p[1]||(p[1]=s("hr",null,null,-1)),l(c,{endpoint:"create-video-effects"}),p[2]||(p[2]=s("hr",null,null,-1)),p[3]||(p[3]=s("h3",{id:"single-image-effect-request-example",tabindex:"-1"},"Single-image Effect Request Example",-1)),p[4]||(p[4]=s("p",null,"Applicable to 216 single-image effects",-1)),l(r,{"code-examples":[{language:"JSON",code:'{\n  "effect_scene": "pet_lion",\n  "input":{\n    "image":"https://p4-kling.klingai.com/bs2/upload-ylab-stunt/c54e463c95816d959602f1f2541c62b2.png?x-kcdn-pid=112452"\n  }\n}'}],"show-header":!1,"max-code-height":"none",class:"md-code-group-panel"}),p[5]||(p[5]=s("h3",{id:"dual-character-effect-request-example",tabindex:"-1"},"Dual-character Effect Request Example",-1)),p[6]||(p[6]=s("p",null,"Applicable to 6 dual-character effects (snow_night_kiss, eternal_kiss, cheers_2026, fight_pro, hug_pro, heart_gesture_pro).",-1)),l(r,{"code-examples":[{language:"JSON",code:'{\n  "effect_scene": "hug_pro",\n  "input": {\n    "images": [\n      "https://example.com/image1.jpg",\n      "https://example.com/image2.jpg"\n    ]\n  }\n}'}],"show-header":!1,"max-code-height":"none",class:"md-code-group-panel"}),p[7]||(p[7]=s("hr",null,null,-1)),l(c,{endpoint:"query-video-effects-single"}),p[8]||(p[8]=s("hr",null,null,-1)),l(c,{endpoint:"query-video-effects-list"})])})};export{o as default};
//# sourceMappingURL=en-KpS5L_ZF.js.map

```
