import {McpServer} from '@modelcontextprotocol/server';
import {StdioServerTransport} from '@modelcontextprotocol/server/stdio';
import {z} from 'zod';
import {dispatch} from './operations.mjs';
import {policy} from './planner.mjs';
const server=new McpServer({name:'agentic-devops',version:'2.0.0-alpha.1'});
for(const action of ['status','plan','validate','preview','rollback','test','benchmark'])server.registerTool('devops_'+action,{description:action+' local deployment artifacts; never deploys or accesses credentials',inputSchema:z.object({input:z.record(z.string(),z.unknown()).optional()}).strict(),annotations:{readOnlyHint:true,destructiveHint:false,openWorldHint:false}},async({input})=>{
 try{const result=await dispatch(action,input??{});return {content:[{type:'text',text:JSON.stringify(result)}],isError:result.passed===false}}
 catch(e){return {isError:true,content:[{type:'text',text:e.message}]}}
});
server.registerResource('policy','ruv://agentic-devops/policy',{mimeType:'application/json'},async uri=>({contents:[{uri:uri.href,text:JSON.stringify(policy)}]}));
await server.connect(new StdioServerTransport(process.stdin,process.stdout,{maxBufferSize:131072}));
