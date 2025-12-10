import { Component, EventEmitter, Input, OnInit, Output, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ClientService } from '../../services/client.service';
import { ToastService } from '../../services/toast.service';

@Component({
    selector: 'app-ticket-modal',
    standalone: true,
    imports: [CommonModule],
    templateUrl: './ticket-modal.component.html',
    styleUrl: './ticket-modal.component.css'
})
export class TicketModalComponent implements OnInit {
    @Input() ticketId!: number;
    @Output() close = new EventEmitter<void>();

    ticket: any = null;
    loading = true;

    private clientService = inject(ClientService);
    private toastService = inject(ToastService);

    ngOnInit() {
        this.loadTicket();
    }

    loadTicket() {
        this.loading = true;
        this.clientService.getTicketDetail(this.ticketId).subscribe({
            next: (data) => {
                this.ticket = data;
                this.loading = false;
            },
            error: (err) => {
                this.toastService.show('Error al cargar boleta', 'error');
                this.loading = false;
                this.close.emit();
            }
        });
    }
}
