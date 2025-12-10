import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class DriverService {
    private http = inject(HttpClient);
    private apiUrl = '/api/driver';

    constructor() { }

    getCurrentTrip(idUsuario: number): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}/current-trip`, { params: { idUsuario: idUsuario.toString() } });
    }

    startTrip(idViaje: number, idUsuario: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/trip/start`, { idViaje, idUsuario });
    }

    endTrip(idViaje: number, idUsuario: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/trip/end`, { idViaje, idUsuario });
    }

    getTripHistory(idUsuario: number): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}/history`, { params: { idUsuario: idUsuario.toString() } });
    }

    getPassengers(idViaje: number, idUsuario: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/trip/passengers?idViaje=${idViaje}&idUsuario=${idUsuario}`);
    }
}
