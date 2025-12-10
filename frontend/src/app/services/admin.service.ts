import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class AdminService {
    private http = inject(HttpClient);
    private apiUrl = '/api/admin';

    constructor() { }

    createCompany(data: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/companies`, data);
    }

    getPendingUsers(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/users/pending`);
    }

    approveUser(idUsuario: number): Observable<any> {
        return this.http.post(`${this.apiUrl}/users/approve`, { idUsuario });
    }

    assignCompany(idUsuario: number, idEmpresa: number): Observable<any> {
        return this.http.post(`${this.apiUrl}/users/assign-company`, { idUsuario, idEmpresa });
    }

    searchUserByDni(dni: string): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}/users/search`, { params: { dni } });
    }

    getCompanyDetails(id: number): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}/companies/${id}`);
    }
}
