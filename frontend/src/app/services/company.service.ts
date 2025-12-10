import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class CompanyService {
    private http = inject(HttpClient);
    private apiUrl = '/api/company';
    private locationUrl = '/api/location'; // Different base for generic locations

    // Drivers
    getDrivers(idEmpresa: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/drivers?idEmpresaTransporte=${idEmpresa}`);
    }

    findUserByDni(dni: string): Observable<any> {
        return this.http.get(`${this.apiUrl}/users/search?dni=${dni}`);
    }

    assignDriver(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/drivers/assign`, payload);
    }

    updateDriver(id: number, payload: any): Observable<any> {
        return this.http.put(`${this.apiUrl}/drivers/${id}`, payload);
    }

    deleteDriver(id: number, idEmpresa: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/drivers/${id}?idEmpresaTransporte=${idEmpresa}`);
    }

    getDriverTrips(idUsuario: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/driver/trips?idUsuario=${idUsuario}`);
    }

    // Vehicles
    getVehicles(idEmpresa: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/vehicles?idEmpresaTransporte=${idEmpresa}`);
    }

    getVehicleTypes(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/vehicle-types`);
    }

    registerVehicle(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/vehicles`, payload);
    }

    updateVehicle(id: number, payload: any): Observable<any> {
        return this.http.put(`${this.apiUrl}/vehicles/${id}`, payload);
    }

    deleteVehicle(id: number, idEmpresa: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/vehicles/${id}?idEmpresaTransporte=${idEmpresa}`);
    }

    // Trips
    getTrips(idEmpresa: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/trips?idEmpresaTransporte=${idEmpresa}`);
    }

    createTrip(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/trips`, payload);
    }

    // Routes
    getRoutes(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/routes`);
    }

    createRoute(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/routes`, payload);
    }

    // Locations (Generic)
    getDepartments(): Observable<any[]> {
        return this.http.get<any[]>(`${this.locationUrl}/departments`);
    }

    getProvinces(idDept: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.locationUrl}/provinces/${idDept}`);
    }

    getDestinationsByProv(idProv: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.locationUrl}/destinations/by-province/${idProv}`);
    }

    getTerminals(): Observable<any[]> {
        return this.http.get<any[]>(`${this.locationUrl}/terminals`);
    }

    // Destination Creation
    createDestination(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/destinations`, payload);
    }

    // Promos
    getPromos(): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/promos`);
    }

    createPromo(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/promos`, payload);
    }

    // Company Details & Banner
    getCompanyDetails(id: number): Observable<any> {
        return this.http.get(`${this.apiUrl}/my-company/${id}`);
    }

    uploadBanner(formData: FormData): Observable<any> {
        return this.http.post(`${this.apiUrl}/banner`, formData);
    }

    // Social Networks
    getSocials(idEmpresa: number): Observable<any[]> {
        return this.http.get<any[]>(`${this.apiUrl}/socials?idEmpresaTransporte=${idEmpresa}`);
    }

    addSocial(payload: any): Observable<any> {
        return this.http.post(`${this.apiUrl}/socials`, payload);
    }

    deleteSocial(id: number, idEmpresa: number): Observable<any> {
        return this.http.delete(`${this.apiUrl}/socials/${id}?idEmpresaTransporte=${idEmpresa}`);
    }
}
