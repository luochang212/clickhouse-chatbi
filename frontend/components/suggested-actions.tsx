'use client';

import { motion } from 'framer-motion';
import { Button } from './ui/button';
import { memo } from 'react';
import type { UseChatHelpers } from '@ai-sdk/react';
import type { VisibilityType } from './visibility-selector';
import type { ChatMessage } from '@/lib/types';

interface SuggestedActionsProps {
  chatId: string;
  sendMessage: UseChatHelpers<ChatMessage>['sendMessage'];
  setInput: (input: string) => void;
  selectedVisibilityType: VisibilityType;
}

function PureSuggestedActions({
  chatId,
  sendMessage,
  setInput,
  selectedVisibilityType,
}: SuggestedActionsProps) {
  const suggestedActions = [
    {
      title: '动画数据库 - 整体统计信息',
      label: '平均分 / 最大值 / 中位数 / 记录数',
      action: '所有动漫的「平均评分」是多少？',
    },
    {
      title: '动画数据库 - 排名信息',
      label: `最高排名 / 最低排名 / 排名前5`,
      action: `评分人数超过一万人的动画中，「排名前 5 」的是？`,
    },
    // {
    //   title: 'What are the advantages',
    //   label: 'of using Next.js?',
    //   action: 'What are the advantages of using Next.js?',
    // },
    // {
    //   title: 'Write code to',
    //   label: `demonstrate djikstra's algorithm`,
    //   action: `Write code to demonstrate djikstra's algorithm`,
    // },
    // {
    //   title: 'Help me write an essay',
    //   label: `about silicon valley`,
    //   action: `Help me write an essay about silicon valley`,
    // },
    // {
    //   title: 'What is the weather',
    //   label: 'in San Francisco?',
    //   action: 'What is the weather in San Francisco?',
    // },
  ];

  return (
    <div
      data-testid="suggested-actions"
      className="grid sm:grid-cols-2 gap-2 w-full"
    >
      {suggestedActions.map((suggestedAction, index) => (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: 20 }}
          transition={{ delay: 0.05 * index }}
          key={`suggested-action-${suggestedAction.title}-${index}`}
          className={index > 1 ? 'hidden sm:block' : 'block'}
        >
          <Button
            variant="ghost"
            // onClick={async () => {
            onClick={(event) => {
              event.preventDefault();
              // window.history.replaceState({}, '', `/chat/${chatId}`);

              // sendMessage({
              //   role: 'user',
              //   parts: [{ type: 'text', text: suggestedAction.action }],
              // });
              setInput(suggestedAction.action);
            }}
            className="text-left border rounded-xl px-4 py-3.5 text-sm flex-1 gap-1 sm:flex-col w-full h-auto justify-start items-start"
          >
            <span className="font-medium">{suggestedAction.title}</span>
            <span className="text-muted-foreground">
              {suggestedAction.label}
            </span>
          </Button>
        </motion.div>
      ))}
    </div>
  );
}

export const SuggestedActions = memo(
  PureSuggestedActions,
  (prevProps, nextProps) => {
    if (prevProps.chatId !== nextProps.chatId) return false;
    if (prevProps.selectedVisibilityType !== nextProps.selectedVisibilityType)
      return false;

    return true;
  },
);
