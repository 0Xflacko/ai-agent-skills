# General Information

- Route: `/global/dev/document-api/apiReference/commonInfo`
- Source markdown path: `/src/docs/apiReference/commonInfo/en.md`
- Source chunk: `https://s16-kling.klingai.com/kos/s101/nlav112918/api-doc/assets/en-Dyq2OaES.js`

## Extracted String Literals

```text
import time
import jwt

ak = "" # fill access key
sk = "" # fill secret key

def encode_jwt_token(ak, sk):
    headers = {
        "alg": "HS256",
        "typ": "JWT"
    }
    payload = {
        "iss": ak,
        "exp": int(time.time()) + 1800, # The valid time, in this example, represents the current time+1800s(30min)
        "nbf": int(time.time()) - 5 # The time when it starts to take effect, in this example, represents the current time -5s
    }
    token = jwt.encode(payload, sk, headers=headers)
    return token

authorization = encode_jwt_token(ak, sk)
print(authorization) # Printing the generated API_TOKEN
package test;

import com.auth0.jwt.JWT;
import com.auth0.jwt.algorithms.Algorithm;

import java.util.Date;
import java.util.HashMap;
import java.util.Map;

public class JWTDemo {
    
    static String ak = ""; // fill access key
    static String sk = ""; // fill secret key
    
    public static void main(String[] args) {
        String token = sign(ak, sk);
        System.out.println(token); // Printing the generated API_TOKEN
    }
    static String sign(String ak,String sk) {
        try {
            Date expiredAt = new Date(System.currentTimeMillis() + 1800*1000); // The valid time, in this example, represents the current time+1800s(30min)
            Date notBefore = new Date(System.currentTimeMillis() - 5*1000); // The time when it starts to take effect, in this example, represents the current time minus 5s
            Algorithm algo = Algorithm.HMAC256(sk);
            Map<String, Object> header = new HashMap<String, Object>();
            header.put("alg", "HS256");
            return JWT.create()
                    .withIssuer(ak)
                    .withHeader(header)
                    .withExpiresAt(expiredAt)
                    .withNotBefore(notBefore)
                    .sign(algo);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
<ul><li>Step-3: Use the API Token generated in Step 2 to assemble the <strong>Authorization</strong> and include it in the <strong>Request Header</strong>. <ul><li>Assembly format: <strong>Authorization</strong> = “Bearer XXX”, where XXX is the API Token generated in Step 2.</li><li>Note: There should be a space between <strong>Bearer</strong> and <strong>XXX</strong>.</li></ul></li></ul><h2 id="error-code" tabindex="-1">Error Code</h2><table><thead><tr><th>HTTP Status Code</th><th>Service Code</th><th>Definition of Service Code</th><th>Explaination of Service Code</th><th>Suggested Solutions</th></tr></thead><tbody><tr><td>200</td><td>0</td><td>Request</td><td>-</td><td>-</td></tr><tr><td>401</td><td>1000</td><td>Authentication failed</td><td>Authentication failed</td><td>Check if the Authorization is correct</td></tr><tr><td>401</td><td>1001</td><td>Authentication failed</td><td>Authorization is empty</td><td>Fill in the correct Authorization in the Request Header</td></tr><tr><td>401</td><td>1002</td><td>Authentication failed</td><td>Authorization is invalid</td><td>Fill in the correct Authorization in the Request Header</td></tr><tr><td>401</td><td>1003</td><td>Authentication failed</td><td>Authorization is not yet valid</td><td>Check the start effective time of the token, wait for it to take effect or reissue</td></tr><tr><td>401</td><td>1004</td><td>Authentication failed</td><td>Authorization has expired</td><td>Check the validity period of the token and reissue it</td></tr><tr><td>429</td><td>1100</td><td>Account exception</td><td>Account exception</td><td>Verifying account configuration information</td></tr><tr><td>429</td><td>1101</td><td>Account exception</td><td>Account in arrears (postpaid scenario)</td><td>Recharge the account to ensure sufficient balance</td></tr><tr><td>429</td><td>1102</td><td>Account exception</td><td>Resource pack depleted or expired (prepaid scenario)</td><td>Purchase additional resource packages, or activate the post-payment service (if available)</td></tr><tr><td>403</td><td>1103</td><td>Account exception</td><td>Unauthorized access to requested resource, such as API/model</td><td>Verifying account permissions</td></tr><tr><td>400</td><td>1200</td><td>Invalid request parameters</td><td>Invalid request parameters</td><td>Check whether the request parameters are correct</td></tr><tr><td>400</td><td>1201</td><td>Invalid request parameters</td><td>Invalid parameters, such as incorrect key or illegal value</td><td>Refer to the specific information in the message field of the returned body and modify the request parameters</td></tr><tr><td>404</td><td>1202</td><td>Invalid request parameters</td><td>The requested method is invalid</td><td>Review the API documentation and use the correct request method</td></tr><tr><td>404</td><td>1203</td><td>Invalid request parameters</td><td>The requested resource does not exist, such as the model</td><td>Refer to the specific information in the message field of the returned body and modify the request parameters</td></tr><tr><td>400</td><td>1300</td><td>Trigger strategy</td><td>Trigger strategy of the platform</td><td>Check if any platform policies have been triggered</td></tr><tr><td>400</td><td>1301</td><td>Trigger strategy</td><td>Trigger the content security policy of the platform</td><td>Check the input content, modify it, and resend the request</td></tr><tr><td>429</td><td>1302</td><td>Trigger strategy</td><td>The API request is too fast, exceeding the platform’s rate limit</td><td>Reduce the request frequency, try again later, or contact customer service to increase the limit</td></tr><tr><td>429</td><td>1303</td><td>Trigger strategy</td><td>Concurrency or QPS exceeds the prepaid resource package limit</td><td>Reduce the request frequency, try again later, or contact customer service to increase the limit</td></tr><tr><td>429</td><td>1304</td><td>Trigger strategy</td><td>Trigger the platform’s IP whitelisting policy</td><td>Contact customer service</td></tr><tr><td>500</td><td>5000</td><td>Internal error</td><td>Server internal error</td><td>Try again later, or contact customer service</td></tr><tr><td>503</td><td>5001</td><td>Internal error</td><td>Server temporarily unavailable, usually due to maintenance</td><td>Try again later, or contact customer service</td></tr><tr><td>504</td><td>5002</td><td>Internal error</td><td>Server internal timeout, usually due to a backlog</td><td>Try again later, or contact customer service</td></tr></tbody></table>
General Information
API Domain
API Authentication
Step-1：Obtain 
Step-2：Every time you request the API, you need to generate an API Token according to the Fixed Encryption Method, Authorization = Bearer <API Token> in Requset Header 
Encryption Method：Follow JWT（Json Web Token, RFC 7519）standard
JWT consists of three parts：Header、Payload、Signature
```

## Raw Chunk Source

```javascript
import{_ as t}from"./ApiCodePanel-CIuPLAIK.js";import{a as e,k as r,b as d,f as n,ar as i,Y as a}from"./index-CyGZTn5T.js";import"./Index-Bsdwq5mu.js";import"./theme-AwbNpswb.js";import"./index-DutzOzEp.js";const o={class:"markdown-body"},s={__name:"en",setup:(s,{expose:c})=>(c({frontmatter:{}}),(s,c)=>{const l=t;return r(),e("div",o,[c[0]||(c[0]=d("h1",{id:"general-information",tabindex:"-1"},"General Information",-1)),c[1]||(c[1]=d("hr",null,null,-1)),c[2]||(c[2]=d("h2",{id:"api-domain",tabindex:"-1"},"API Domain",-1)),n(l,{"code-examples":[{language:"Bash",code:"https://api-singapore.klingai.com"}],"show-header":!1,"max-code-height":"none",class:"md-code-group-panel"}),c[3]||(c[3]=d("h2",{id:"api-authentication",tabindex:"-1"},"API Authentication",-1)),c[4]||(c[4]=d("ul",null,[d("li",null,[a("Step-1：Obtain "),d("strong",null,"AccessKey"),a(" + "),d("strong",null,"SecretKey")]),d("li",null,[a("Step-2：Every time you request the API, you need to generate an API Token according to the Fixed Encryption Method, Authorization = Bearer <API Token> in Requset Header "),d("ul",null,[d("li",null,"Encryption Method：Follow JWT（Json Web Token, RFC 7519）standard"),d("li",null,"JWT consists of three parts：Header、Payload、Signature")])])],-1)),n(l,{"code-examples":[{language:"Python",code:'import time\nimport jwt\n\nak = "" # fill access key\nsk = "" # fill secret key\n\ndef encode_jwt_token(ak, sk):\n    headers = {\n        "alg": "HS256",\n        "typ": "JWT"\n    }\n    payload = {\n        "iss": ak,\n        "exp": int(time.time()) + 1800, # The valid time, in this example, represents the current time+1800s(30min)\n        "nbf": int(time.time()) - 5 # The time when it starts to take effect, in this example, represents the current time -5s\n    }\n    token = jwt.encode(payload, sk, headers=headers)\n    return token\n\nauthorization = encode_jwt_token(ak, sk)\nprint(authorization) # Printing the generated API_TOKEN'},{language:"Java",code:'package test;\n\nimport com.auth0.jwt.JWT;\nimport com.auth0.jwt.algorithms.Algorithm;\n\nimport java.util.Date;\nimport java.util.HashMap;\nimport java.util.Map;\n\npublic class JWTDemo {\n    \n    static String ak = ""; // fill access key\n    static String sk = ""; // fill secret key\n    \n    public static void main(String[] args) {\n        String token = sign(ak, sk);\n        System.out.println(token); // Printing the generated API_TOKEN\n    }\n    static String sign(String ak,String sk) {\n        try {\n            Date expiredAt = new Date(System.currentTimeMillis() + 1800*1000); // The valid time, in this example, represents the current time+1800s(30min)\n            Date notBefore = new Date(System.currentTimeMillis() - 5*1000); // The time when it starts to take effect, in this example, represents the current time minus 5s\n            Algorithm algo = Algorithm.HMAC256(sk);\n            Map<String, Object> header = new HashMap<String, Object>();\n            header.put("alg", "HS256");\n            return JWT.create()\n                    .withIssuer(ak)\n                    .withHeader(header)\n                    .withExpiresAt(expiredAt)\n                    .withNotBefore(notBefore)\n                    .sign(algo);\n        } catch (Exception e) {\n            e.printStackTrace();\n            return null;\n        }\n    }\n}'}],"max-code-height":"none",class:"md-code-group-panel"}),c[5]||(c[5]=i('<ul><li>Step-3: Use the API Token generated in Step 2 to assemble the <strong>Authorization</strong> and include it in the <strong>Request Header</strong>. <ul><li>Assembly format: <strong>Authorization</strong> = “Bearer XXX”, where XXX is the API Token generated in Step 2.</li><li>Note: There should be a space between <strong>Bearer</strong> and <strong>XXX</strong>.</li></ul></li></ul><h2 id="error-code" tabindex="-1">Error Code</h2><table><thead><tr><th>HTTP Status Code</th><th>Service Code</th><th>Definition of Service Code</th><th>Explaination of Service Code</th><th>Suggested Solutions</th></tr></thead><tbody><tr><td>200</td><td>0</td><td>Request</td><td>-</td><td>-</td></tr><tr><td>401</td><td>1000</td><td>Authentication failed</td><td>Authentication failed</td><td>Check if the Authorization is correct</td></tr><tr><td>401</td><td>1001</td><td>Authentication failed</td><td>Authorization is empty</td><td>Fill in the correct Authorization in the Request Header</td></tr><tr><td>401</td><td>1002</td><td>Authentication failed</td><td>Authorization is invalid</td><td>Fill in the correct Authorization in the Request Header</td></tr><tr><td>401</td><td>1003</td><td>Authentication failed</td><td>Authorization is not yet valid</td><td>Check the start effective time of the token, wait for it to take effect or reissue</td></tr><tr><td>401</td><td>1004</td><td>Authentication failed</td><td>Authorization has expired</td><td>Check the validity period of the token and reissue it</td></tr><tr><td>429</td><td>1100</td><td>Account exception</td><td>Account exception</td><td>Verifying account configuration information</td></tr><tr><td>429</td><td>1101</td><td>Account exception</td><td>Account in arrears (postpaid scenario)</td><td>Recharge the account to ensure sufficient balance</td></tr><tr><td>429</td><td>1102</td><td>Account exception</td><td>Resource pack depleted or expired (prepaid scenario)</td><td>Purchase additional resource packages, or activate the post-payment service (if available)</td></tr><tr><td>403</td><td>1103</td><td>Account exception</td><td>Unauthorized access to requested resource, such as API/model</td><td>Verifying account permissions</td></tr><tr><td>400</td><td>1200</td><td>Invalid request parameters</td><td>Invalid request parameters</td><td>Check whether the request parameters are correct</td></tr><tr><td>400</td><td>1201</td><td>Invalid request parameters</td><td>Invalid parameters, such as incorrect key or illegal value</td><td>Refer to the specific information in the message field of the returned body and modify the request parameters</td></tr><tr><td>404</td><td>1202</td><td>Invalid request parameters</td><td>The requested method is invalid</td><td>Review the API documentation and use the correct request method</td></tr><tr><td>404</td><td>1203</td><td>Invalid request parameters</td><td>The requested resource does not exist, such as the model</td><td>Refer to the specific information in the message field of the returned body and modify the request parameters</td></tr><tr><td>400</td><td>1300</td><td>Trigger strategy</td><td>Trigger strategy of the platform</td><td>Check if any platform policies have been triggered</td></tr><tr><td>400</td><td>1301</td><td>Trigger strategy</td><td>Trigger the content security policy of the platform</td><td>Check the input content, modify it, and resend the request</td></tr><tr><td>429</td><td>1302</td><td>Trigger strategy</td><td>The API request is too fast, exceeding the platform’s rate limit</td><td>Reduce the request frequency, try again later, or contact customer service to increase the limit</td></tr><tr><td>429</td><td>1303</td><td>Trigger strategy</td><td>Concurrency or QPS exceeds the prepaid resource package limit</td><td>Reduce the request frequency, try again later, or contact customer service to increase the limit</td></tr><tr><td>429</td><td>1304</td><td>Trigger strategy</td><td>Trigger the platform’s IP whitelisting policy</td><td>Contact customer service</td></tr><tr><td>500</td><td>5000</td><td>Internal error</td><td>Server internal error</td><td>Try again later, or contact customer service</td></tr><tr><td>503</td><td>5001</td><td>Internal error</td><td>Server temporarily unavailable, usually due to maintenance</td><td>Try again later, or contact customer service</td></tr><tr><td>504</td><td>5002</td><td>Internal error</td><td>Server internal timeout, usually due to a backlog</td><td>Try again later, or contact customer service</td></tr></tbody></table>',3))])})};export{s as default};
//# sourceMappingURL=en-Dyq2OaES.js.map

```
