import { useEffect, useState } from "react";

export const Toast = ({ message, duration = 3000, onClose }) => {
  const [visible, setVisible] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => {
      setVisible(false);
      if (onClose) onClose();
    }, duration);

    return () => clearTimeout(timer);
  }, [duration, onClose]);

  if (!visible) return null;

  return (
    <div className="fixed top-4 right-4 z-50">
      <div className="bg-gray-800 text-white px-4 py-2 rounded-lg shadow-lg border border-gray-700 max-w-xs">
        {message}
      </div>
    </div>
  );
};
