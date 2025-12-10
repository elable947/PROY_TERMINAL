import { Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { ClientService } from '../../services/client.service';
import { TicketModalComponent } from '../ticket-modal/ticket-modal.component';

@Component({
    selector: 'app-my-trips',
    standalone: true,
    imports: [CommonModule, RouterModule, TicketModalComponent],
    templateUrl: './my-trips.component.html',
    styleUrl: './my-trips.component.css'
})
export class MyTripsComponent implements OnInit {
    private clientService = inject(ClientService);

    history: any[] = [];
    loading = true;
    showModal = false;
    selectedTicketId: number | null = null;

    ngOnInit() {
        this.loadHistory();
    }

    loadHistory() {
        this.loading = true;
        this.clientService.getHistory().subscribe({
            next: (data) => {
                this.history = data;
                this.loading = false;
            },
            error: (err) => {
                console.error(err);
                this.loading = false;
            }
        });
    }

    openTicket(id: number) {
        this.selectedTicketId = id;
        this.showModal = true;
    }

    closeModal() {
        this.showModal = false;
        this.selectedTicketId = null;
    }

    cancelReservation(idBoleto: number, event: Event) {
        event.stopPropagation();
        if (!confirm('¿Estás seguro de cancelar esta reserva? El asiento quedará libre.')) return;

        this.loading = true;
        this.clientService.cancelReservation(idBoleto).subscribe({
            next: () => {
                alert('Reserva cancelada exitosamente.');
                this.loadHistory();
            },
            error: (err) => {
                alert(err.error?.error || 'Error al cancelar');
                this.loading = false;
            }
        });
    }
}
