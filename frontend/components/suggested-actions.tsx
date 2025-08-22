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
      action: '所有动画的「平均评分」是多少？',
    },
    {
      title: '动画数据库 - 排名信息',
      label: `最高排名 / 最低排名 / 排名前5`,
      action: `评分人数超过三千人的动画中，「排名前 5 」的是？`,
    },
    {
      title: '动画数据库 - 条件过滤',
      label: '评分人数 / 动画数 / 评分 / 开始播出时间',
      action: '制作过至少 3 部评分在 8.8 以上的动画的工作室有哪些？',
    },
    {
      title: '动画数据库 - 帕累托最优',
      label: `多目标优化 / 非支配解 / 效率前沿`,
      action: `找出在「评分」和「评分人数」两个维度上的帕累托最优解集？`,
    },
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
            //   window.history.replaceState({}, '', `/chat/${chatId}`);

            //   sendMessage({
            //     role: 'user',
            //     parts: [{ type: 'text', text: suggestedAction.action }],
            //   });
            // }}
            onClick={(event) => {
              event.preventDefault();
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
