import { initializeApp } from 'firebase/app';
import { getAnalytics } from 'firebase/analytics';
import { getAuth, GoogleAuthProvider } from 'firebase/auth';

const firebaseConfig = {
  apiKey: "AIzaSyAc6UBqVPwSKkZfcD-4P-7J7Ccp6roa6Wk",
  authDomain: "pensionpath-c6103.firebaseapp.com",
  projectId: "pensionpath-c6103",
  storageBucket: "pensionpath-c6103.firebasestorage.app",
  messagingSenderId: "691327467394",
  appId: "1:691327467394:web:3bbad3e3e8217bb9e5199b",
  measurementId: "G-DVJ0HXZT74"
};

export const app = initializeApp(firebaseConfig);
export const analytics = getAnalytics(app);
export const auth = getAuth(app);
export const googleProvider = new GoogleAuthProvider();
