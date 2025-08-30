// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';
import { redirect } from '@sveltejs/kit';
import { getMeService } from './routes/services/auth';

export const handle: Handle = async ({ event, resolve }) => {
  const token = event.cookies.get('token');

  if ((event.url.pathname.startsWith('/invoice') || event.url.pathname.startsWith('/receipt')) && !token) {
    throw redirect(302, '/login');
  }

  if (event.url.pathname.startsWith('/login') && token) {
    throw redirect(302, '/invoice');
  }

  if (event.url.pathname.startsWith('/users')) {
    if (!token) {
      throw redirect(302, '/login'); 
    }

    let res;
    try {
      res = await getMeService(token); 
    } catch (error) {
      console.error(error);
      throw redirect(302, '/login'); 
    }

    if (!res.isSuperuser) {
      throw redirect(302, '/invoice'); 
    }
  }

  return resolve(event);
};
