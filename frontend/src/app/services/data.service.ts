import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class DataService {
    private http = inject(HttpClient);
    private apiUrl = '/api/data';

    constructor() { }

    getDestinos(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/destinos`);
    }

    getEmpresas(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/empresas`);
    }

    getPaises(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/paises`);
    }
}
