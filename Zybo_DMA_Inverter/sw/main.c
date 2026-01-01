 #include "xaxidma.h"
#include "xparameters.h"
#include "xuartps.h"
#include "xil_printf.h"
#include "xil_cache.h"


#define DMA_BASE XPAR_AXI_DMA_0_BASEADDR
#define UART_BASE XPAR_XUARTPS_0_BASEADDR


#define IMG_W 28
#define IMG_H 28
#define IMG_BYTES (IMG_W * IMG_H)


#define TX_BUF 0x01000000
#define RX_BUF 0x02000000


XAxiDma AxiDma;
XUartPs Uart;


u8 *Tx = (u8*)TX_BUF;
u8 *Rx = (u8*)RX_BUF;


void uart_recv(u8 *buf, int len)
{
    int i = 0;
    while (i < len) {
        if (XUartPs_IsReceiveData(Uart.Config.BaseAddress)) {
            buf[i++] = XUartPs_ReadReg(
                Uart.Config.BaseAddress,
                XUARTPS_FIFO_OFFSET
            );
        }
    }
}


void uart_send(u8 *buf, int len)
{
    int i = 0;
    while (i < len) {
        i += XUartPs_Send(&Uart, &buf[i], len - i);
    }
}


int main()
{
    /* UART init */
    XUartPs_Config *Ucfg = XUartPs_LookupConfig(UART_BASE);
    XUartPs_CfgInitialize(&Uart, Ucfg, Ucfg->BaseAddress);
    XUartPs_SetBaudRate(&Uart, 115200);


    /* DMA init */
    XAxiDma_Config *Dcfg = XAxiDma_LookupConfig(DMA_BASE);
    XAxiDma_CfgInitialize(&AxiDma, Dcfg);


    /* Receive image */
    uart_recv(Tx, IMG_BYTES);


    Xil_DCacheFlushRange((UINTPTR)Tx, IMG_BYTES);
    Xil_DCacheFlushRange((UINTPTR)Rx, IMG_BYTES);


    /* Start DMA */
    XAxiDma_SimpleTransfer(
        &AxiDma,
        (UINTPTR)Rx,
        IMG_BYTES,
        XAXIDMA_DEVICE_TO_DMA
    );


    XAxiDma_SimpleTransfer(
        &AxiDma,
        (UINTPTR)Tx,
        IMG_BYTES,
        XAXIDMA_DMA_TO_DEVICE
    );


    while (XAxiDma_Busy(&AxiDma, XAXIDMA_DEVICE_TO_DMA));
    while (XAxiDma_Busy(&AxiDma, XAXIDMA_DMA_TO_DEVICE));


    Xil_DCacheInvalidateRange((UINTPTR)Rx, IMG_BYTES);


    /* Send back result */
    uart_send(Rx, IMG_BYTES);


    while (1);
}
