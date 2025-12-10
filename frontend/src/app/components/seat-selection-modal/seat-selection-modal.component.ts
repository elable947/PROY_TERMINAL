import { Component, EventEmitter, Input, Output, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClientService } from '../../services/client.service';
import { ToastService } from '../../services/toast.service';

@Component({
    selector: 'app-seat-selection-modal',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './seat-selection-modal.component.html',
    styleUrl: './seat-selection-modal.component.css'
})
export class SeatSelectionModalComponent implements OnInit {
    @Input() tripId!: number;
    @Input() trip: any; // Receive trip details
    @Output() close = new EventEmitter<void>();
    @Output() purchaseSuccess = new EventEmitter<any>();

    private clientService = inject(ClientService);
    private toastService = inject(ToastService);

    seats: any[] = [];
    paymentMethods: any[] = [];
    selectedSeatId: number | null = null;
    selectedPaymentId: number | null = null;
    loading = true;
    buying = false;

    // View State: 'SELECTION' | 'PAYMENT'
    viewState: 'SELECTION' | 'PAYMENT' = 'SELECTION';

    get selectedSeatNum() {
        return this.seats.find(s => s.idAsiento === this.selectedSeatId)?.numeroAsiento;
    }

    ngOnInit() {
        this.loadSeats();
        this.loadPaymentMethods();
    }

    loadSeats() {
        this.loading = true;
        this.clientService.getSeats(this.tripId).subscribe({
            next: (data) => {
                this.seats = data;
                this.loading = false;
            },
            error: (err) => {
                console.error(err);
                this.toastService.show('Error al cargar asientos', 'error');
                this.loading = false;
            }
        });
    }

    loadPaymentMethods() {
        this.clientService.getPaymentMethods().subscribe(data => this.paymentMethods = data);
    }

    selectSeat(seat: any) {
        if (!seat.disponible) return;
        this.selectedSeatId = seat.idAsiento;
    }

    goToPayment() {
        if (!this.selectedSeatId) return;
        this.viewState = 'PAYMENT';
    }

    backToSelection() {
        this.viewState = 'SELECTION';
        this.selectedPaymentId = null;
    }

    processAction() {
        if (!this.selectedSeatId || !this.selectedPaymentId) return;

        // Find method name
        const method = this.paymentMethods.find(m => m.idMetodoPago == this.selectedPaymentId);
        const isCash = method?.nombreMetodoPago?.toUpperCase().includes('EFECTIVO');

        if (isCash) {
            // Cash -> Reservation
            this.confirmReservation();
        } else {
            // Other -> Purchase
            this.confirmPurchase(this.selectedPaymentId);
        }
    }

    private formatDate(dateStr: string): string {
        if (!dateStr) return '';
        const d = new Date(dateStr);
        return `${d.toLocaleDateString()} a las ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`;
    }

    confirmPurchase(paymentId: number) {
        this.buying = true;
        const payload = {
            idViaje: this.tripId,
            idAsiento: this.selectedSeatId,
            idMetodoPago: paymentId
        };

        this.clientService.purchaseTicket(payload).subscribe({
            next: (res) => {
                const dateText = this.trip ? this.formatDate(this.trip.fechaSalida) : '';
                this.toastService.show(`¡Pasaje COMPRADO! Viaje: ${dateText}`, 'success');
                this.buying = false;
                this.purchaseSuccess.emit(res);
                this.close.emit();
            },
            error: (err) => {
                this.buying = false;
                const msg = err.error?.message || err.error?.error || 'Error en la compra';
                this.toastService.show(msg, 'error');
                this.loadSeats();
                this.viewState = 'SELECTION';
            }
        });
    }

    confirmReservation() {
        this.buying = true;
        const payload = {
            idViaje: this.tripId,
            idAsiento: this.selectedSeatId
        };

        this.clientService.reserveTicket(payload).subscribe({
            next: (res) => {
                const dateText = this.trip ? this.formatDate(this.trip.fechaSalida) : '';
                this.toastService.show(`¡Pasaje RESERVADO! Viaje: ${dateText} (Pago en Efectivo)`, 'success'); // Changed to success (green) or info
                this.buying = false;
                this.purchaseSuccess.emit(res);
                this.close.emit();
            },
            error: (err) => {
                this.buying = false;
                const msg = err.error?.message || err.error?.error || 'Error en la reserva';
                this.toastService.show(msg, 'error');
                this.loadSeats();
                this.viewState = 'SELECTION';
            }
        });
    }
}
