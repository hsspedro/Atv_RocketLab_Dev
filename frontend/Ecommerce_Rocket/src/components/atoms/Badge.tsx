import type { ReactNode } from 'react';

interface BadgeProps {
  children: ReactNode;
  variant?: 'primary' | 'success' | 'warning';
}

export default function Badge({ children, variant = 'primary' }: BadgeProps) {
  const variants = {
    primary: 'bg-brand-100 text-brand-700',
    success: 'bg-emerald-100 text-emerald-700',
    warning: 'bg-amber-100 text-amber-700',
  };

  return (
    <span className={`inline-flex rounded-full px-3 py-1 text-xs font-semibold ${variants[variant]}`}>
      {children}
    </span>
  );
}
