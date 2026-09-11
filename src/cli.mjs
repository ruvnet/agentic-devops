#!/usr/bin/env node
import {dispatch} from './operations.mjs';
const action=process.argv[2]??'status';
try{
 if(action==='mcp')await import('./mcp.mjs');
 else{
  let raw='';
  if(!['status','test','benchmark'].includes(action)){
   const timer=setTimeout(()=>{process.stderr.write('Input deadline exceeded\n');process.exit(2)},10000);
   for await(const chunk of process.stdin){raw+=chunk;if(Buffer.byteLength(raw)>65536)throw new Error('Input too large')};clearTimeout(timer);
  }
  const result=await dispatch(action,raw?JSON.parse(raw):{});process.stdout.write(JSON.stringify(result,null,2)+'\n');
  if(result.passed===false)process.exitCode=1;
 }
}catch(e){process.stderr.write(e.message+'\n');process.exit(2)}
