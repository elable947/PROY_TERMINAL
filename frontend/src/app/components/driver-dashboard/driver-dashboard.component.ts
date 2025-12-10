import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DriverService } from '../../services/driver.service';
import { AuthService } from '../../services/auth.service';
import { ToastService } from '../../services/toast.service';

@Component({
    selector: 'app-driver-dashboard',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './driver-dashboard.component.html',
    styleUrls: ['./driver-dashboard.component.css']
})
export class DriverDashboardComponent implements OnInit {
    private driverService = inject(DriverService);
    private authService = inject(AuthService);
    private toastService = inject(ToastService);

    currentTrip: any = null;
    tripHistory: any[] = []; // New
    currentUser: any = null;
    loading = false;

    // Modal State
    confirmModal = {
        isOpen: false,
        title: '',
        message: '',
        icon: '',
        action: () => { }
    };

    ngOnInit() {
        this.authService.currentUser$.subscribe(user => {
            this.currentUser = user;
            if (user && user.idUsuario) {
                this.loadCurrentTrip();
                this.loadHistory();
            }
        });
    }

    loadCurrentTrip() {
        this.loading = true;
        this.driverService.getCurrentTrip(this.currentUser.idUsuario).subscribe({
            next: (data) => {
                this.currentTrip = data;
                this.loading = false;
            },
            error: (err) => {
                console.error(err);
                this.loading = false;
            }
        });
    }

    loadHistory() {
        this.driverService.getTripHistory(this.currentUser.idUsuario).subscribe({
            next: (data) => this.tripHistory = data,
            error: (err) => console.error('History error', err)
        });
    }

    openConfirm(title: string, message: string, icon: string, action: () => void) {
        this.confirmModal = { isOpen: true, title, message, icon, action };
    }

    closeConfirm() {
        this.confirmModal.isOpen = false;
    }

    confirmAction() {
        if (this.confirmModal.action) {
            this.confirmModal.action();
        }
        // Do not verify isOpen, just close it.
        this.confirmModal.isOpen = false;
        this.confirmModal.action = () => { }; // Reset action to avoid double triggers
    }

    startTrip() {
        if (!this.currentTrip) return;
        this.openConfirm(
            'Iniciar Viaje',
            '¿Estás listo para iniciar el recorrido? El estado cambiará a "En Ruta".',
            'fa-route',
            () => {
                this.driverService.startTrip(this.currentTrip.idViaje, this.currentUser.idUsuario).subscribe({
                    next: () => {
                        this.toastService.show('¡Viaje iniciado! Buen camino.', 'success');
                        this.loadCurrentTrip();
                    },
                    error: (err) => this.toastService.show(err.error?.error || 'Error al iniciar viaje', 'error')
                });
            }
        );
    }

    endTrip() {
        if (!this.currentTrip) return;
        this.openConfirm(
            'Finalizar Viaje',
            '¿Has llegado a tu destino? Esto marcará el viaje como completado.',
            'fa-flag-checkered',
            () => {
                this.driverService.endTrip(this.currentTrip.idViaje, this.currentUser.idUsuario).subscribe({
                    next: () => {
                        this.toastService.show('Viaje finalizado correctamente.', 'success');
                        this.loadCurrentTrip();
                        this.loadHistory();
                    },
                    error: (err) => this.toastService.show(err.error?.error || 'Error al finalizar viaje', 'error')
                });
            }
        );
    }

    // Passenger Modal
    passengers: any[] = [];
    showPassengersModal = false;

    openPassengersModal() {
        if (!this.currentTrip) return;
        this.driverService.getPassengers(this.currentTrip.idViaje, this.currentUser.idUsuario).subscribe({
            next: (data) => {
                this.passengers = data;
                this.showPassengersModal = true;
            },
            error: (err) => this.toastService.show('Error al cargar pasajeros', 'error')
        });
    }

    closePassengersModal() {
        this.showPassengersModal = false;
    }
}
