interface InputProps {
  label?: string;
  value: string;
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  placeholder?: string;
  type?: string;
  required?: boolean;
}

export default function Input({
  label,
  value,
  onChange,
  placeholder,
  type = 'text',
  required = false,
}: InputProps) {
  return (
    <label className="flex flex-col gap-2 text-sm font-medium text-slate-700">
      {label && (
        <span>
          {label} {required ? '*' : ''}
        </span>
      )}
      <input
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="rounded-2xl border border-slate-300 bg-white px-4 py-3 text-slate-900 shadow-sm outline-none transition focus:border-brand-500 focus:ring-2 focus:ring-brand-100"
      />
    </label>
  );
}
