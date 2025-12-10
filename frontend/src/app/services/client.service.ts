import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ClientService {
    private http = inject(HttpClient);
    private apiUrl = '/api/client';

    getSeats(idViaje: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/trips/${idViaje}/seats`);
    }

    purchaseTicket(payload: any): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/purchase`, payload);
    }

    reserveTicket(payload: any): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/reserve`, payload);
    }

    getPaymentMethods(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/payment-methods`);
    }

    getHistory(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/history`);
    }

    getTicketDetail(idBoleto: number): Observable<any> {
        return this.http.get<any>(`${this.apiUrl}/ticket/${idBoleto}`);
    }

    cancelReservation(idBoleto: number): Observable<any> {
        return this.http.post<any>(`${this.apiUrl}/cancel-reservation`, { idBoleto });
    }
}
