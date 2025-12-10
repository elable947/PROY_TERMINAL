import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class PublicService {
    private http = inject(HttpClient);
    private apiUrl = '/api/public';

    getCompanies(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/companies`);
    }

    getPublicTrips(idDestino?: number, idEmpresa?: number): Observable<any[]> {
        let params = new HttpParams();
        if (idDestino) params = params.set('idDestino', idDestino);
        if (idEmpresa) params = params.set('idEmpresa', idEmpresa);
        return this.http.get<any[]>(`${this.apiUrl}/trips`, { params });
    }

    getDestinations(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/destinations`);
    }
}
