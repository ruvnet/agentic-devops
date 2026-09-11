import test from 'node:test';import assert from 'node:assert/strict';
import {Client} from '@modelcontextprotocol/client';import {StdioClientTransport} from '@modelcontextprotocol/client/stdio';import {fixture} from '../src/planner.mjs';
test('official SDK stdio discovers tools and executes plan validation rollback negatives',async()=>{
 const transport=new StdioClientTransport({command:process.execPath,args:['src/mcp.mjs'],env:{PATH:process.env.PATH},stderr:'pipe'});const client=new Client({name:'e2e',version:'1'});await client.connect(transport);
 try{const list=await client.listTools();assert.equal(list.tools.length,7);const call=async(name,input)=>client.callTool({name:'devops_'+name,arguments:{input}});const p=await call('plan',fixture);assert.equal(p.isError,false);const bundle=JSON.parse(p.content[0].text);assert.equal((await call('validate',bundle)).isError,false);assert.equal((await call('plan',{...fixture,command:'id'})).isError,true);assert.equal((await call('test',{})).isError,true);assert.equal((await client.readResource({uri:'ruv://agentic-devops/policy'})).contents.length,1)}finally{await client.close()}
});
