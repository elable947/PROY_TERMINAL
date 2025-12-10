import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap, BehaviorSubject } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
    providedIn: 'root'
})
export class AuthService {
    private http = inject(HttpClient);
    private router = inject(Router);
    private apiUrl = '/api/auth';
    private currentUserKey = 'currentUser';

    // Reactive state
    private currentUserSubject = new BehaviorSubject<any>(null);
    currentUser$ = this.currentUserSubject.asObservable();

    constructor() {
        const stored = localStorage.getItem(this.currentUserKey);
        if (stored) {
            this.currentUserSubject.next(JSON.parse(stored));
        }
    }

    login(credentials: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/login`, credentials).pipe(
            tap((response: any) => {
                if (response.user) {
                    localStorage.setItem(this.currentUserKey, JSON.stringify(response.user));
                    if (response.token) localStorage.setItem('token', response.token);
                    this.currentUserSubject.next(response.user);
                }
            })
        );
    }

    register(userData: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/register`, userData);
    }

    logout() {
        localStorage.removeItem(this.currentUserKey);
        localStorage.removeItem('token');
        this.currentUserSubject.next(null);
        this.router.navigate(['/login']);
    }

    updateProfile(data: any): Observable<any> {
        return this.http.put(`${this.apiUrl}/profile`, data).pipe(
            tap((response: any) => {
                if (response.user) {
                    localStorage.setItem(this.currentUserKey, JSON.stringify(response.user));
                    this.currentUserSubject.next(response.user);
                }
            })
        );
    }

    getCurrentUser() {
        const userStr = localStorage.getItem(this.currentUserKey);
        return userStr ? JSON.parse(userStr) : null;
    }

    isLoggedIn(): boolean {
        return !!this.getCurrentUser();
    }
}
