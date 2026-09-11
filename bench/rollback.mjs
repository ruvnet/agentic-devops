import * as base from './baseline-planner.mjs';import * as candidate from '../src/planner.mjs';import {performance} from 'node:perf_hooks';import assert from 'node:assert/strict';
const inputs=Array.from({length:100},(_,i)=>{const previous=base.plan({...base.fixture,name:'app-'+i,replicas:1+i%20});const current=base.plan({...base.fixture,name:'app-'+i,replicas:1+i%20,image:'ghcr.io/example/app@sha256:'+'c'.repeat(64)});return {current,previous,expectedCurrent:current.sha256}});
for(const x of inputs)assert.deepEqual(base.rollback(x),candidate.rollback(x));
for(let n=0;n<1000;n++){base.rollback(inputs[n%100]);candidate.rollback(inputs[n%100])}
function run(fn){const times=[];for(let i=0;i<3000;i++){const t=performance.now();fn(inputs[i%100]);times.push(performance.now()-t)}times.sort((a,b)=>a-b);return{medianMs:times[1500],p95Ms:times[2850]}}
const rounds=[];for(let n=0;n<5;n++){let b,c;if(n%2){c=run(candidate.rollback);b=run(base.rollback)}else{b=run(base.rollback);c=run(candidate.rollback)}rounds.push({baseline:b,candidate:c})}
console.log(JSON.stringify({baseline:'6d27e365da0f72746c18aa8f28e0baafa457b9d4',node:process.version,inputs:100,iterationsPerRound:3000,rounds,equivalentOutputs:true},null,2));
