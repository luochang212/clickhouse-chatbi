'use client';

interface CodeBlockProps {
  node: any;
  inline: boolean;
  className: string;
  children: any;
}

export function CodeBlock({
  node,
  inline,
  className,
  children,
  ...props
}: CodeBlockProps) {
  if (!inline) {
    return (
      <span className="block w-full max-w-full overflow-x-auto border border-zinc-200 dark:border-zinc-700 rounded-xl bg-zinc-50 dark:bg-zinc-900">
        <code
          {...props}
          className={`block text-sm p-4 dark:text-zinc-50 text-zinc-900 whitespace-pre bg-transparent font-mono`}
          style={{ maxWidth: '100%', maxHeight: 'none', height: 'auto', minWidth: 0, margin: 0, display: 'block' }}
        >
          {children}
        </code>
      </span>
    );
  } else {
    return (
      <code
        className={`${className} text-sm bg-zinc-100 dark:bg-zinc-800 py-0.5 px-1 rounded-md`}
        {...props}
      >
        {children}
      </code>
    );
  }
}
