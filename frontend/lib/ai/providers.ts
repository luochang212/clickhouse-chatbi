import {
  customProvider,
  extractReasoningMiddleware,
  wrapLanguageModel,
} from 'ai';
import { createOpenAICompatible } from '@ai-sdk/openai-compatible';
import {
  artifactModel,
  chatModel,
  reasoningModel,
  titleModel,
} from './models.test';
import { isTestEnvironment } from '../constants';

// 阿里云百炼配置
const bailian = createOpenAICompatible({
  name: 'bailian',
  apiKey: process.env.DASHSCOPE_API_KEY,
  baseURL: 'https://dashscope.aliyuncs.com/compatible-mode/v1',  // process.env.DASHSCOPE_BASE_URL
  headers: {
    'X-DashScope-Compat-Mode': 'enabled'
  },
});

// ClickHouse Agent API 配置
const clickhouseAgent = createOpenAICompatible({
  name: 'clickhouse-agent',
  apiKey: 'dummy-key',
  baseURL: 'http://mcp-service:8001/v1',
});

export const myProvider = isTestEnvironment
  ? customProvider({
      languageModels: {
        'chat-model': chatModel,
        'chat-model-reasoning': reasoningModel,
        'title-model': titleModel,
        'artifact-model': artifactModel,
      },
    })
  : customProvider({
      languageModels: {
        'chat-model': clickhouseAgent('clickhouse-agent'),
        'chat-model-reasoning': wrapLanguageModel({
          model: clickhouseAgent('clickhouse-agent'),
          middleware: extractReasoningMiddleware({ tagName: 'think' }),
        }),
        'title-model': bailian('qwen-plus'),  // bailian('qwen-max')  bailian('qwen-turbo')
        'artifact-model': bailian('qwen-plus'),
      },
      imageModels: {
        'small-model': bailian.imageModel('qwen-vl-plus'),
      },
    });
