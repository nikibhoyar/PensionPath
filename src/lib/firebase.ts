import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyBKZTQbmSZwP0d4lkTkT7PmpLHsXVHLMLs",
  authDomain: "pension-path.firebaseapp.com",
  projectId: "pension-path",
  storageBucket: "pension-path.firebasestorage.app",
  messagingSenderId: "1070935957532",
  appId: "1:1070935957532:web:0b01f46ac29cfde0d83fd9",
  measurementId: "G-LJWZTM3HB9"
};

export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();