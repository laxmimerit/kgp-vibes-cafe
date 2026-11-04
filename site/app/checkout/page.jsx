'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

export default function CheckoutRedirect() {
  const router = useRouter();

  useEffect(() => {
    router.replace('/cart');
  }, [router]);

  return (
    <div className="bg-background font-body-md text-on-surface p-8 text-center min-h-[50vh] flex flex-col items-center justify-center">
      <p>
        Redirecting to{' '}
        <Link href="/cart" className="text-primary underline font-semibold">
          Order Checkout
        </Link>
        ...
      </p>
    </div>
  );
}
