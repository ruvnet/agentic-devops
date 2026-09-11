import {spawn} from 'node:child_process';
import {performance} from 'node:perf_hooks';
import {fileURLToPath} from 'node:url';
import {plan,validate,preview,rollback,policy,fixture} from './planner.mjs';
let busy=false;
export function benchmark(){const times=[];for(let i=0;i<1000;i++){const t=performance.now();validate(plan(fixture));times.push(performance.now()-t)}times.sort((a,b)=>a-b);return {iterations:1000,unit:'ms',median:times[500],p95:times[950],scope:'Local generation and policy validation; no registry or cluster traffic'};}
export function tests(){
 if(process.env.AGENTIC_DEVOPS_ALLOW_TESTS!=='1')throw new Error('Local operator must enable AGENTIC_DEVOPS_ALLOW_TESTS=1');
 if(busy)throw new Error('Validation already running');busy=true;
 return new Promise((resolve,reject)=>{let output='',done=false;const p=spawn(process.execPath,['--test','tests/planner.test.mjs'],{cwd:fileURLToPath(new URL('../',import.meta.url)),env:{PATH:process.env.PATH},stdio:['ignore','pipe','pipe'],detached:process.platform!=='win32'});
 const finish=(error)=>{if(done)return;done=true;clearTimeout(timer);busy=false;error?reject(error):resolve({passed:p.exitCode===0,output})};
 const kill=()=>{try{process.kill(-p.pid,'SIGKILL')}catch{p.kill('SIGKILL')}};
 const timer=setTimeout(()=>{kill();finish(new Error('Validation deadline exceeded'))},30000);
 for(const stream of [p.stdout,p.stderr])stream.on('data',x=>{output+=x;if(Buffer.byteLength(output)>65536){kill();finish(new Error('Validation output limit exceeded'))}});
 p.on('error',finish);p.on('close',()=>finish());
 });
}
export async function dispatch(action,input={}){
 if(Buffer.byteLength(JSON.stringify(input))>65536)throw new Error('Input too large');
 if(action==='status')return {project:'agentic-devops',version:'2.0.0-alpha.1',policy};
 if(action==='plan')return plan(input);
 if(action==='validate')return validate(input);
 if(action==='preview')return preview(input);
 if(action==='rollback')return rollback(input);
 if(Object.keys(input).length)throw new Error('This operation takes no arguments');
 if(action==='test')return tests();
 if(action==='benchmark')return benchmark();
 throw new Error('Unknown action');
}
