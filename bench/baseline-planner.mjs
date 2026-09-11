import {createHash} from 'node:crypto';
export const policy = Object.freeze({version:1,network:false,execution:false,credentials:false,maxInputBytes:65536,maxReplicas:20,artifacts:['Dockerfile','deployment.json','service.json','network-policy.json','ci.yml'],promotion:'operator-reviewed'});
const digest = x => createHash('sha256').update(x).digest('hex');
const json = x => JSON.stringify(x,null,2)+'\n';
function fail(s){throw new Error(s)}
function obj(x,keys){if(!x||typeof x!=='object'||Array.isArray(x)||Object.keys(x).some(k=>!keys.includes(k)))fail('Unexpected object or field');}
const name = x=> typeof x==='string'&&/^[a-z](?:[a-z0-9-]{0,38}[a-z0-9])?$/.test(x);
const image = x => typeof x==='string' && x.length<=240 && /^[a-z0-9]+(?:[._-][a-z0-9]+)*(?:\/[a-z0-9]+(?:[._-][a-z0-9]+)*)*@sha256:[a-f0-9]{64}$/.test(x);
export function spec(x){
 obj(x,['name','namespace','image','baseImage','port','replicas','cpuMillis','memoryMiB']);
 if(!name(x.name)||!name(x.namespace)||!image(x.image)||!image(x.baseImage))fail('Names and digest-pinned image references required');
 const s={name:x.name,namespace:x.namespace,image:x.image,baseImage:x.baseImage,port:x.port??8080,replicas:x.replicas??2,cpuMillis:x.cpuMillis??250,memoryMiB:x.memoryMiB??128};
 for(const [k,min,max] of [['port',1024,65535],['replicas',1,20],['cpuMillis',10,4000],['memoryMiB',16,8192]])if(!Number.isSafeInteger(s[k])||s[k]<min||s[k]>max)fail('Resource limit outside policy: '+k);
 return s;
}
export function plan(input){
 const s=spec(input), labels={app:s.name};
 const container={name:s.name,image:s.image,ports:[{containerPort:s.port}],securityContext:{allowPrivilegeEscalation:false,readOnlyRootFilesystem:true,runAsNonRoot:true,runAsUser:10001,capabilities:{drop:['ALL']},seccompProfile:{type:'RuntimeDefault'}},resources:{requests:{cpu:s.cpuMillis+'m',memory:s.memoryMiB+'Mi'},limits:{cpu:s.cpuMillis+'m',memory:s.memoryMiB+'Mi'}},readinessProbe:{tcpSocket:{port:s.port},initialDelaySeconds:2,periodSeconds:5},livenessProbe:{tcpSocket:{port:s.port},initialDelaySeconds:10,periodSeconds:10}};
 const deployment={apiVersion:'apps/v1',kind:'Deployment',metadata:{name:s.name,namespace:s.namespace},spec:{replicas:s.replicas,revisionHistoryLimit:3,selector:{matchLabels:labels},template:{metadata:{labels},spec:{automountServiceAccountToken:false,containers:[container]}}}};
 const service={apiVersion:'v1',kind:'Service',metadata:{name:s.name,namespace:s.namespace},spec:{type:'ClusterIP',selector:labels,ports:[{port:s.port,targetPort:s.port}]}};
 const network={apiVersion:'networking.k8s.io/v1',kind:'NetworkPolicy',metadata:{name:s.name,namespace:s.namespace},spec:{podSelector:{matchLabels:labels},policyTypes:['Ingress','Egress'],ingress:[{from:[{podSelector:{}}],ports:[{protocol:'TCP',port:s.port}]}],egress:[]}};
 const artifacts={'Dockerfile':`FROM ${s.baseImage}\nWORKDIR /app\nCOPY --chown=10001:10001 app/ /app/\nUSER 10001:10001\nEXPOSE ${s.port}\nENTRYPOINT ["/app/server"]\n`,'deployment.json':json(deployment),'service.json':json(service),'network-policy.json':json(network),'ci.yml':`name: Artifact verification\non: [push, pull_request]\npermissions:\n  contents: read\njobs:\n  verify:\n    runs-on: ubuntu-latest\n    steps:\n      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683\n        with:\n          persist-credentials: false\n      - run: docker build --network=none --tag local-artifact .\n`};
 return {version:1,spec:s,artifacts,sha256:digest(json(artifacts)),effects:[],warnings:['Container contract: supply an executable /app/server compatible with the chosen base image.','NetworkPolicy requires a supporting CNI; egress is denied.','Image digest syntax is checked; registry existence, signatures and vulnerabilities require deployment qualification.']};
}
export function validate(bundle){
 obj(bundle,['version','spec','artifacts','sha256','effects','warnings']);
 const expected=plan(bundle.spec);
 if(JSON.stringify(bundle)!==JSON.stringify(expected))fail('Bundle differs from canonical approved policy output');
 return {valid:true,sha256:expected.sha256,executionAuthorized:false};
}
export function preview({before,after}){
 validate(before);validate(after);
 if(before.spec.name!==after.spec.name||before.spec.namespace!==after.spec.namespace)fail('Resource identity cannot change');
 const changed=policy.artifacts.filter(k=>before.artifacts[k]!==after.artifacts[k]);
 return {from:before.sha256,to:after.sha256,changed,resourceIdentity:{name:after.spec.name,namespace:after.spec.namespace},executionAuthorized:false};
}
export function rollback({current,previous,expectedCurrent}){
 validate(current);validate(previous);
 if(current.sha256!==expectedCurrent)fail('Stale rollback: current digest mismatch');
 preview({before:current,after:previous});
 return {target:previous,from:current.sha256,executionAuthorized:false};
}
export const fixture={name:'demo-app',namespace:'demo-team',image:'ghcr.io/example/app@sha256:'+'a'.repeat(64),baseImage:'gcr.io/distroless/static-debian12@sha256:'+'b'.repeat(64)};
