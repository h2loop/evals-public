# H2LooP v0.1 Coder: Embedded Systems Benchmark Report

## TL;DR
We comprehensively evaluated three models on a diverse set of embedded C tasks that embedded developers encounter, drawing from real-world workflows and rubric—requirement coverage (prompt, goal, objectives), raw-code compilation with minimal scaffolding, and code quality (correctness, safety, portability). H2LooP v0.1 Coder, trained via human-in-the-loop domain curation and rubric-driven iteration, achieves approximately 80–85% coverage while compiling reliably (surpassing SOTA Open-source GPT OSS-120B with less than 30x size) and far outpacing similarly-sized Gemma‑4B’s basic primitives. Results are indicative, not exhaustive of all scenarios in production embedded developement with HIL, ongoing work continues to broaden tasks, hardware families, and statistical reporting.

## Models brief

We handpicked 2 models to compare our model with - the best open-source model of comparitive size (Google's Gemma 4B-instruct) and one structurally similar open-source large model to one used in GitHub Copilot (GPT OSS-120B).
- H2LooP v0.1 Coder: Domain-specific, small language model (SLM) trained on embedded systems corpus with human-in-the-loop curation
- GPT OSS 120B (120B): Large State-of-the-art open-source LLM, general-purpose 
- Gemma-4B-IT (4B): General-purpose instruction-tuned SLM.

Key findings:
- Coverage of requirements: H2LooP ~80–85% (prompt, goal, objectives), GPT OSS 120B ~50%, Gemma-4B-IT ~20% (basic primitives)
- Compilation success from raw model code: GPT OSS 120B is highest, H2LooP is a close second, Gemma-4B-IT is lowest
- H2LooP’s embedded-specific training yields the most comprehensive solutions across MCU, peripheral, RTOS, bootloader, and embedded Linux scenarios


## Dataset Overview
This benchmark draws tasks and evaluation cues from a curated dataset that captures real-world embedded workflows, in sync with domain experts who provided us with
- Prompt: task statement aligned to practical MCU/Linux development
- Description: scope and constraints (e.g., device families, register-level expectations)
- Goal: end-state behavior (e.g., full-duplex SPI exchange, robust bootloading)
- Objectives: concrete acceptance criteria used for scoring (e.g., GPIO AF setup, protocol sequencing, error paths)
- Difficulty: relative complexity (from bare-metal bring-up to Linux and RTOS)
- Category: domain taxonomy (MCU/Bare-Metal, Peripheral Programming, Bootloader Development, FreeRTOS Integration, Sensor Fusion, Embedded Linux)

We use this structured schema to derive requirement checklists and reproducible scoring without revealing dataset size. Items span MCU register configuration, peripheral protocols, bootloader safety, RTOS tasking, and Linux /proc parsing and synchronization, reflecting the diversity an embedded systems programmer commonly encounters.



### Human-in-the-Loop (H2LooP) Development
- Domain prompt set curated by embedded engineers
- Multi-stage instruction tuning with rubric-based scoring for correctness, completeness, and safety
- Iterative red-teaming for hardware corner cases and platform specificity

### Benchmark Design and Scope
- Source: Representative tasks drawn from real-world embedded workflows (diverse domains; sample set is still evolving each day)
- Measures: requirement coverage (prompt/goal/objectives), compile success, and code quality rubrics
- Outputs: side-by-side code samples and metrics for each prompt across all models
- Scope: These results are indicative of model behavior on common embedded patterns; a broader evaluation is planned to expand tasks, hardware families, and statistical reporting


## Metrics Overview

- Requirement coverage: H2LooP ~80–85% | GPT OSS 120B ~50% | Gemma-4B-IT ~20%
- Compilation success (raw model output): GPT OSS 120B highest, H2LooP close second, Gemma-4B-IT lowest
- Code quality rubric (correctness, safety, portability): H2LooP leads on average across prompts

## Categorical Success rate 

Note: Coverage reflects proportion of prompt, goal, and objectives satisfied by the raw model output. Compilation reflects whether the unedited output compiled successfully after adding only includes and a minimal main if required.

| Example | H2LooP Coverage | H2LooP Compile | GPT OSS 120B Coverage | GPT OSS 120B Compile | Gemma-4B-IT Coverage | Gemma-4B-IT Compile |
|---|---:|---:|---:|---:|---:|---:|
| MCU and Bare-Metal | 84% | 93% | 55% | 99% | 20% | 68% |
| Peripheral Programming | 83% | 88% | 50% | 95% | 18% | 62% |
| Bootloader Development | 82% | 96% | 48% | 95% | 22% | 61% |
| FreeRTOS Integration | 85% | 91% | 52% | 94% | 19% | 63% |
| Sensor Fusion-Based Applications | 84% | 90% | 49% | 91% | 21% | 64% |
| Embedded Linux | 83% | 87% | 51% | 91% | 20% | 65% |


## Why H2LooP Code Is Superior (Comparative Code and Summary)

The following table summarizes, for each showcased example, why H2LooP’s code is superior relative to GPT OSS 120B and Gemma‑4B‑IT. H2LooP consistently implements register‑level correctness, protocol sequencing, safety checks, and concurrency patterns that align with embedded best practices.

| Example | H2LooP v0.1 Coder | GPT OSS 120B | Gemma‑4B‑IT |
|---|---|---|---|
| SPI Master Full‑Duplex | Complete GPIO AF config (SCK/MISO/MOSI/NSS), master mode, CPOL/CPHA, soft NSS, error checks, loopback self‑test | Partial init; missing GPIO AF and CPOL/CPHA rationale; minimal transfer routine | HAL‑style placeholder; no register‑level detail |
| I²C Master (Polling+IRQ) | START/ADDR/Tx/Rx/STOP, ACK/NACK, timeouts, event+error ISRs, RX ring buffer | Polling write only; interrupts and error paths omitted | Primitive stub; no sequencing |
| UART Bootloader (Flash Write) | Framed UART RX, CRC32 verify, page erase + aligned halfword programming, metadata write, vector relocation | Simple write loop without erase or CRC/metadata; risk of corrupting flash | Sketch only; no flash controller usage or integrity checks |
| FreeRTOS Sensor Fusion | Per‑sensor tasks, PIR ISR->notification, queue to fusion, mutex logging, stable cadence | Two producer tasks + queue; no PIR ISR or mutex/log policy | Single polling loop; no RTOS primitives |
| Linux Resource Monitor (per‑thread) | Parses /proc/[pid]/task/*/stat and smaps; mutex‑protected snapshot; periodic sampling | Reads /proc/stat totals; misses per‑thread view; no mutex | Placeholder with TODOs |
| Linux Resource Monitor (multi‑thread UI) | Sampler + renderer threads, condition variable, signal‑safe shutdown | Single‑threaded; blocking and no shutdown coordination | Outline only |

Why H2LooP excels: Domain‑guided training with human‑in‑the‑loop evaluation optimizes for embedded‑specific needs: register‑accurate init, protocol timing/ordering, safety (timeouts, integrity checks), and real RTOS/Linux synchronization patterns. This yields comprehensive requirement coverage with strong compile reliability, while general‑purpose models omit critical embedded details or produce only high‑level primitives.

## Side-by-Side Examples

### 1) SPI Master Full-Duplex Transfer
Prompt: "Generate code to configure SPI master, perform full-duplex transfer"

- H2LooP v0.1 Coder: Complete GPIO alt-function setup, clock gating, CPOL/CPHA, frame size, robust TX/RX with error handling, and a loopback self-test.
```c
#include <stdint.h>
#include <stdbool.h>
#include "stm32f10x.h"

static inline void spi_gpio_init(void){
    RCC->APB2ENR |= RCC_APB2ENR_IOPAEN | RCC_APB2ENR_AFIOEN; // Enable GPIOA + AFIO
    // PA5=SCK, PA6=MISO, PA7=MOSI, PA4=NSS
    // PA5: AF push-pull 50MHz: CRL MODE5=0b11, CNF5=0b10
    GPIOA->CRL &= ~((0xF << (5*4)) | (0xF << (6*4)) | (0xF << (7*4)) | (0xF << (4*4)));
    GPIOA->CRL |=  ((0xB << (5*4)) | /* MODE=11, CNF=10 */
                    (0x4 << (6*4)) | /* MISO input floating */
                    (0xB << (7*4)) | /* MOSI AF PP */
                    (0x3 << (4*4)));  /* NSS GPIO out 50MHz */
    // Deassert NSS high
    GPIOA->BSRR = (1u << 4);
}

void spi_init(void){
    RCC->APB2ENR |= RCC_APB2ENR_SPI1EN; // Enable SPI1 clock
    spi_gpio_init();
    // Configure: master, BR=fPCLK/8, CPOL=1, CPHA=1 (example), SSM+SSI for soft NSS, 8-bit
    SPI1->CR1 = SPI_CR1_MSTR | SPI_CR1_BR_1 | SPI_CR1_CPOL | SPI_CR1_CPHA | SPI_CR1_SSM | SPI_CR1_SSI;
    SPI1->CR2 = 0; // Simple polling mode
    SPI1->CR1 |= SPI_CR1_SPE;
}

static inline void spi_assert_nss(void){ GPIOA->BSRR = (1u << (4 + 16)); }
static inline void spi_deassert_nss(void){ GPIOA->BSRR = (1u << 4); }

static inline bool spi_check_errors(void){
    uint32_t sr = SPI1->SR;
    // Check OVR or MODF
    return (sr & (SPI_SR_OVR | SPI_SR_MODF)) == 0;
}

uint8_t spi_transfer(uint8_t byte){
    while(!(SPI1->SR & SPI_SR_TXE)); // wait TX empty
    *(volatile uint8_t*)&SPI1->DR = byte;
    while(!(SPI1->SR & SPI_SR_RXNE)); // wait RX not empty
    uint8_t r = *(volatile uint8_t*)&SPI1->DR;
    (void)spi_check_errors();
    return r;
}

void spi_xfer_burst(const uint8_t* tx, uint8_t* rx, uint32_t n){
    spi_assert_nss();
    for(uint32_t i=0;i<n;i++){
        uint8_t t = tx ? tx[i] : 0xFF;
        uint8_t r = spi_transfer(t);
        if(rx) rx[i] = r;
    }
    spi_deassert_nss();
}

bool spi_loopback_selftest(void){
    static const uint8_t pattern[4] = {0x55,0xAA,0x12,0x34};
    uint8_t out[4], in[4];
    for(int i=0;i<4;i++){ out[i]=pattern[i]; }
    spi_xfer_burst(out, in, 4);
    for(int i=0;i<4;i++) if(in[i]!=out[i]) return false;
    return true;
}
```
- GPT OSS 120B: Partial setup; missing GPIO AF configuration and CPOL/CPHA alignment; transfers may succeed in basic cases but are not robust.
```c
#include <stdint.h>
#include "stm32f10x.h"
void spi_init(void){
    RCC->APB2ENR |= RCC_APB2ENR_SPI1EN;
    SPI1->CR1 = SPI_CR1_MSTR | SPI_CR1_BR_1;
    SPI1->CR1 |= SPI_CR1_SPE;
}
uint8_t spi_transfer(uint8_t b){ while(!(SPI1->SR & SPI_SR_TXE)); SPI1->DR=b; while(!(SPI1->SR & SPI_SR_RXNE)); return SPI1->DR; }
```
- Gemma-4B-IT: Minimal primitive implementation (no GPIO AF setup, default mode, polling transfers only).
```c
#include <stdint.h>
#include "stm32f10x.h"

void spi_init(void)
{
    RCC->APB2ENR |= RCC_APB2ENR_SPI1EN;   // enable SPI1 clock only
    SPI1->CR1 = SPI_CR1_MSTR;             // master, default CPOL/CPHA
    SPI1->CR1 |= SPI_CR1_SPE;             // enable SPI
}

uint8_t spi_transfer(uint8_t b)
{
    while ((SPI1->SR & SPI_SR_TXE) == 0) {}
    SPI1->DR = b;
    while ((SPI1->SR & SPI_SR_RXNE) == 0) {}
    return (uint8_t)SPI1->DR;
}
```

### 2) I²C Master Driver (Polling then Interrupt)
Prompt: "Develop I²C driver (master Tx/Rx) in polling mode, then interrupt mode"

- H2LooP v0.1 Coder: Full START/ADDR/Tx/Rx/STOP sequence, ACK/NACK, event/error ISRs, and an RX ring buffer.
```c
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "stm32f10x.h"

#define I2C_TIMEOUT 100000u

static volatile uint8_t rxbuf[128];
static volatile uint16_t rx_head=0, rx_tail=0;
static inline void rx_push(uint8_t b){ uint16_t n=(rx_head+1u)%sizeof(rxbuf); if(n!=rx_tail){ rxbuf[rx_head]=b; rx_head=n; } }
static inline bool rx_pop(uint8_t* b){ if(rx_tail==rx_head) return false; *b=rxbuf[rx_tail]; rx_tail=(rx_tail+1u)%sizeof(rxbuf); return true; }

void i2c1_init(uint32_t pclk1){
    RCC->APB1ENR |= RCC_APB1ENR_I2C1EN; RCC->APB2ENR |= RCC_APB2ENR_IOPBEN | RCC_APB2ENR_AFIOEN;
    // PB6=SCL, PB7=SDA as AF open-drain
    GPIOB->CRL &= ~((0xF<<(6*4)) | (0xF<<(7*4)));
    GPIOB->CRL |=  ((0xF<<(6*4)) | (0xF<<(7*4))); // MODE=11 50MHz, CNF=11 AF OD
    I2C1->CR2 = (pclk1/1000000u); // MHz
    I2C1->CCR = (pclk1/200000u);  // 100kHz standard (2*100k)
    I2C1->TRISE = (pclk1/1000000u)+1u; // 1000ns
    I2C1->CR1 = I2C_CR1_PE;
    // Enable event/error interrupts
    I2C1->CR2 |= I2C_CR2_ITEVTEN | I2C_CR2_ITBUFEN | I2C_CR2_ITERREN;
    NVIC_EnableIRQ(I2C1_EV_IRQn); NVIC_EnableIRQ(I2C1_ER_IRQn);
}

static bool i2c_start(uint8_t addr_rw){
    I2C1->CR1 |= I2C_CR1_START; // generate START
    uint32_t t=I2C_TIMEOUT; while(!(I2C1->SR1 & I2C_SR1_SB) && --t); if(!t) return false;
    (void)I2C1->SR1; // clear SB by read then write DR
    I2C1->DR = addr_rw; // address + R/W
    t=I2C_TIMEOUT; while(!(I2C1->SR1 & I2C_SR1_ADDR) && --t){ if(I2C1->SR1 & I2C_SR1_AF){ I2C1->SR1 &= ~I2C_SR1_AF; return false; } }
    if(!t) return false;
    (void)I2C1->SR1; (void)I2C1->SR2; // clear ADDR
    return true;
}

static bool i2c_stop(void){ I2C1->CR1 |= I2C_CR1_STOP; return true; }

bool i2c_write_poll(uint8_t addr7, const uint8_t* data, uint16_t n){
    if(!i2c_start((addr7<<1)|0)) return false;
    for(uint16_t i=0;i<n;i++){
        I2C1->DR = data[i];
        uint32_t t=I2C_TIMEOUT; while(!(I2C1->SR1 & I2C_SR1_BTF) && --t){ if(I2C1->SR1 & I2C_SR1_AF){ I2C1->SR1 &= ~I2C_SR1_AF; i2c_stop(); return false; } }
        if(!t){ i2c_stop(); return false; }
    }
    i2c_stop();
    return true;
}

bool i2c_read_poll(uint8_t addr7, uint8_t* data, uint16_t n){
    if(n==0) return true;
    I2C1->CR1 |= I2C_CR1_ACK; // ACK all but last
    if(!i2c_start((addr7<<1)|1)) return false;
    for(uint16_t i=0;i<n;i++){
        if(i==n-1){ I2C1->CR1 &= ~I2C_CR1_ACK; I2C1->CR1 |= I2C_CR1_STOP; }
        uint32_t t=I2C_TIMEOUT; while(!(I2C1->SR1 & I2C_SR1_RXNE) && --t); if(!t) return false;
        data[i] = I2C1->DR;
    }
    return true;
}

void I2C1_EV_IRQHandler(void){
    uint32_t sr1 = I2C1->SR1; (void)I2C1->SR2; // read SR2 to release SCL
    if(sr1 & I2C_SR1_RXNE){ uint8_t b = I2C1->DR; rx_push(b); }
    if(sr1 & I2C_SR1_TXE){ /* ready to send next byte if using IRQ-driven TX */ }
    if(sr1 & I2C_SR1_BTF){ /* byte transfer finished: schedule next operation */ }
}

void I2C1_ER_IRQHandler(void){
    uint32_t sr1 = I2C1->SR1;
    if(sr1 & I2C_SR1_AF){ I2C1->SR1 &= ~I2C_SR1_AF; }
    if(sr1 & I2C_SR1_BERR){ I2C1->SR1 &= ~I2C_SR1_BERR; }
    if(sr1 & I2C_SR1_ARLO){ I2C1->SR1 &= ~I2C_SR1_ARLO; }
    if(sr1 & I2C_SR1_OVR){ I2C1->SR1 &= ~I2C_SR1_OVR; }
}
```
- GPT OSS 120B: Polling write works; interrupt path incomplete, no error IRQ.
```c
#include <stdint.h>
#include "stm32f10x.h"
int i2c_write(uint8_t addr7, const uint8_t* data, int n){
    I2C1->CR1 |= I2C_CR1_START; while(!(I2C1->SR1 & I2C_SR1_SB)); (void)I2C1->SR1; I2C1->DR=(addr7<<1)|0;
    while(!(I2C1->SR1 & I2C_SR1_ADDR)); (void)I2C1->SR1; (void)I2C1->SR2;
    for(int i=0;i<n;i++){ I2C1->DR=data[i]; while(!(I2C1->SR1 & I2C_SR1_BTF)); }
    I2C1->CR1 |= I2C_CR1_STOP; return 0;
}
```
- Gemma-4B-IT: Minimal polling transmit (no error handling, no interrupts).
```c
#include <stdint.h>
#include "stm32f10x.h"

int i2c_tx(uint8_t addr7, const uint8_t* data, int n)
{
    // START
    I2C1->CR1 |= I2C_CR1_START;
    while ((I2C1->SR1 & I2C_SR1_SB) == 0) {}
    (void)I2C1->SR1;
    // Address (write)
    I2C1->DR = (addr7 << 1) | 0;
    while ((I2C1->SR1 & I2C_SR1_ADDR) == 0) {}
    (void)I2C1->SR1; (void)I2C1->SR2;
    // Write bytes
    for (int i = 0; i < n; i++) {
        I2C1->DR = data[i];
        while ((I2C1->SR1 & I2C_SR1_BTF) == 0) {}
    }
    // STOP
    I2C1->CR1 |= I2C_CR1_STOP;
    return 0;
}
```


### 3) UART Bootloader: Write Image to Flash
Prompt: Implement UART-based bootloader that writes image to Flash

- H2LooP v0.1 Coder: UART RX with ring buffer and framed packets, page erase + aligned Flash programming, CRC gate, and vector relocation.
```c
#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include "stm32f10x.h"

#define FLASH_PAGE_SIZE   1024u
#define APP_BASE_ADDR     0x08004000u
#define META_ADDR         0x08003C00u

static inline void flash_unlock(void){ if(FLASH->CR & FLASH_CR_LOCK){ FLASH->KEYR=0x45670123; FLASH->KEYR=0xCDEF89AB; } }
static inline void flash_lock(void){ FLASH->CR |= FLASH_CR_LOCK; }
static inline bool flash_wait(void){ while(FLASH->SR & FLASH_SR_BSY){} return (FLASH->SR & (FLASH_SR_PGERR|FLASH_SR_WRPRTERR))==0; }
static bool flash_erase_page(uint32_t addr){ flash_unlock(); FLASH->CR |= FLASH_CR_PER; FLASH->AR=addr; FLASH->CR |= FLASH_CR_STRT; bool ok=flash_wait(); FLASH->CR &= ~FLASH_CR_PER; flash_lock(); return ok; }
static bool flash_program_halfword(uint32_t addr, uint16_t hw){ flash_unlock(); FLASH->CR |= FLASH_CR_PG; *(volatile uint16_t*)addr = hw; bool ok=flash_wait(); FLASH->CR &= ~FLASH_CR_PG; flash_lock(); return ok; }

static bool flash_write(uint32_t dst, const uint8_t* src, uint32_t len){
    // erase pages covering [dst, dst+len)
    uint32_t startPage = dst & ~(FLASH_PAGE_SIZE-1u);
    uint32_t endAddr = dst + len;
    for(uint32_t a=startPage; a<endAddr; a+=FLASH_PAGE_SIZE){ if(!flash_erase_page(a)) return false; }
    // program halfwords
    for(uint32_t i=0;i<len;i+=2){
        uint16_t hw = src[i] | ((i+1<len?src[i+1]:0xFFu)<<8);
        if(!flash_program_halfword(dst+i, hw)) return false;
    }
    return true;
}

// Simple CRC32 (poly 0xEDB88320)
static uint32_t crc32_update(uint32_t c, uint8_t b){ c ^= b; for(int i=0;i<8;i++){ c = (c & 1)? (0xEDB88320u ^ (c>>1)) : (c>>1); } return c; }
static uint32_t crc32(const uint8_t* p, uint32_t n){ uint32_t c=0xFFFFFFFFu; for(uint32_t i=0;i<n;i++) c=crc32_update(c,p[i]); return c^0xFFFFFFFFu; }

// Framed packets: [len(2)][payload...]
#define UART_RX_SZ 256
static volatile uint8_t rx[UART_RX_SZ]; static volatile uint16_t rx_h=0, rx_t=0;
static inline void rx_isr_push(uint8_t b){ uint16_t n=(rx_h+1u)%UART_RX_SZ; if(n!=rx_t){ rx[rx_h]=b; rx_h=n; } }
static bool rx_pop(uint8_t* b){ if(rx_t==rx_h) return false; *b=rx[rx_t]; rx_t=(rx_t+1u)%UART_RX_SZ; return true; }

void USART1_IRQHandler(void){ if(USART1->SR & USART_SR_RXNE){ rx_isr_push((uint8_t)USART1->DR); } }

static bool read_exact(uint8_t* buf, uint16_t n){ for(uint16_t i=0;i<n;i++){ uint32_t t=100000; while(!rx_pop(&buf[i]) && --t); if(!t) return false; } return true; }

bool boot_receive_and_program(void){
    // read image length
    uint8_t hdr[2]; if(!read_exact(hdr,2)) return false; uint16_t len = (uint16_t)hdr[0] | ((uint16_t)hdr[1]<<8);
    if(len==0 || len > 64*1024) return false; // sanity
    // read payload + crc
    static uint8_t img[64*1024]; if(!read_exact(img,len)) return false; uint8_t crcb[4]; if(!read_exact(crcb,4)) return false; 
    uint32_t want = (uint32_t)crcb[0] | ((uint32_t)crcb[1]<<8) | ((uint32_t)crcb[2]<<16) | ((uint32_t)crcb[3]<<24);
    uint32_t got = crc32(img,len); if(got != want) return false;
    // program
    if(!flash_write(APP_BASE_ADDR, img, len)) return false;
    // write metadata (length + crc)
    uint8_t meta[8] = { (uint8_t)len, (uint8_t)(len>>8), (uint8_t)got, (uint8_t)(got>>8), (uint8_t)(got>>16), (uint8_t)(got>>24), 0, 0 };
    if(!flash_write(META_ADDR, meta, 8)) return false;
    return true;
}

typedef void (*app_entry_t)(void);
void boot_jump_to_app(void){
    uint32_t *vt = (uint32_t*)APP_BASE_ADDR;
    uint32_t sp = vt[0]; uint32_t pc = vt[1];
    __disable_irq(); SCB->VTOR = APP_BASE_ADDR;
    __set_MSP(sp); ((app_entry_t)pc)();
}
```
- GPT OSS 120B: Implements a basic write loop but omits erase-before-write and CRC/metadata; may corrupt Flash if page not erased.
```c
#include <stdint.h>
#include "stm32f10x.h"
void flash_prog(uint32_t addr, const uint8_t* data, int n){ (void)FLASH->SR; for(int i=0;i<n;i+=2){ *(volatile uint16_t*)(addr+i) = (uint16_t)data[i] | ((i+1<n?data[i+1]:0)<<8); } }
```
- Gemma-4B-IT: Minimal memory copy stub (no erase, no CRC/metadata) to illustrate primitive behavior.
```c
#include <stdint.h>

static uint8_t app_buf[1024];

int bootloader_stub(const uint8_t* src, int len)
{
    if (len < 0 || len > (int)sizeof(app_buf)) {
        return -1;
    }
    for (int i = 0; i < len; ++i) {
        app_buf[i] = src[i];
    }
    return 0; // copied to RAM only
}
```

### 4) FreeRTOS Sensor Fusion (BME280 + ADXL345 + GPS + PIR)
Prompt: Develop FreeRTOS-based sensor fusion task (BME280 + ADXL345 + GPS + PIR)

- H2LooP v0.1 Coder: Separate tasks per sensor, ISR -> task notification for PIR, queue to fusion task, mutex-protected logging, 1 Hz cadence.
```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
#include "semphr.h"
#include <stdio.h>
#include <string.h>

typedef struct { float temp_c, pressure_pa, humidity; } bme280_t;
typedef struct { float ax, ay, az; } adxl345_t;
typedef struct { double lat, lon; float speed_mps; } gps_t;
typedef struct { int motion; } pir_t;
typedef struct { bme280_t bme; adxl345_t acc; gps_t gps; pir_t pir; } fusion_sample_t;

static QueueHandle_t qFusion;
static SemaphoreHandle_t mLog;
static TaskHandle_t hPirConsumer;

// Mock sensor reads
static void bme280_read(bme280_t* o){ o->temp_c=25.0f; o->pressure_pa=101325.0f; o->humidity=50.0f; }
static void adxl345_read(adxl345_t* o){ o->ax=0.01f; o->ay=0.02f; o->az=0.98f; }
static void gps_read(gps_t* o){ o->lat=37.4219; o->lon=-122.0840; o->speed_mps=0.0f; }

// PIR ISR (pseudo)
void EXTI0_IRQHandler(void){ BaseType_t hpw=pdFALSE; vTaskNotifyGiveFromISR(hPirConsumer,&hpw); portYIELD_FROM_ISR(hpw); }

static void vBME280Task(void* arg){ (void)arg; fusion_sample_t s; memset(&s,0,sizeof s);
    for(;;){ bme280_read(&s.bme); xQueueSend(qFusion,&s,portMAX_DELAY); vTaskDelay(pdMS_TO_TICKS(1000)); } }
static void vADXLTask(void* arg){ (void)arg; fusion_sample_t s; memset(&s,0,sizeof s);
    for(;;){ adxl345_read(&s.acc); xQueueSend(qFusion,&s,portMAX_DELAY); vTaskDelay(pdMS_TO_TICKS(200)); } }
static void vGPSTask(void* arg){ (void)arg; fusion_sample_t s; memset(&s,0,sizeof s);
    for(;;){ gps_read(&s.gps); xQueueSend(qFusion,&s,portMAX_DELAY); vTaskDelay(pdMS_TO_TICKS(1000)); } }
static void vPIRTask(void* arg){ (void)arg; fusion_sample_t s; memset(&s,0,sizeof s);
    for(;;){ ulTaskNotifyTake(pdTRUE, portMAX_DELAY); s.pir.motion=1; xQueueSend(qFusion,&s,0); s.pir.motion=0; } }

static void vFusionTask(void* arg){ (void)arg; fusion_sample_t s;
    for(;;){ if(xQueueReceive(qFusion,&s,portMAX_DELAY)==pdTRUE){
            xSemaphoreTake(mLog,portMAX_DELAY);
            printf("T=%.2fC P=%.0fPa H=%.1f%% AX=%.2f AY=%.2f AZ=%.2f LAT=%.5f LON=%.5f V=%.2fmps PIR=%d\n",
                s.bme.temp_c,s.bme.pressure_pa,s.bme.humidity,
                s.acc.ax,s.acc.ay,s.acc.az,
                s.gps.lat,s.gps.lon,s.gps.speed_mps,
                s.pir.motion);
            xSemaphoreGive(mLog);
        } }
}

void app_start(void){
    qFusion = xQueueCreate(16,sizeof(fusion_sample_t));
    mLog = xSemaphoreCreateMutex();
    xTaskCreate(vBME280Task,"bme",512,NULL,1,NULL);
    xTaskCreate(vADXLTask,"acc",512,NULL,1,NULL);
    xTaskCreate(vGPSTask,"gps",512,NULL,1,NULL);
    xTaskCreate(vPIRTask,"pir",512,NULL,2,&hPirConsumer);
    xTaskCreate(vFusionTask,"fuse",1024,NULL,1,NULL);
    vTaskStartScheduler();
}
```
- GPT OSS 120B: Two producer tasks with a queue; no PIR interrupt, no mutex for logging.
```c
#include "FreeRTOS.h"
#include "task.h"
#include "queue.h"
static QueueHandle_t q;
static void vTask1(void*arg){ for(;;){ /* read bme */ xQueueSend(q,"BME",portMAX_DELAY); vTaskDelay(1000); } }
static void vTask2(void*arg){ for(;;){ /* read adxl */ xQueueSend(q,"ADXL",portMAX_DELAY); vTaskDelay(200); } }
static void vConsumer(void*arg){ char buf[8]; for(;;){ xQueueReceive(q,&buf,portMAX_DELAY); /* print */ } }
void app(void){ q=xQueueCreate(8,sizeof(char[8])); xTaskCreate(vTask1,"t1",256,NULL,1,NULL); xTaskCreate(vTask2,"t2",256,NULL,1,NULL); xTaskCreate(vConsumer,"c",256,NULL,1,NULL); vTaskStartScheduler(); }
```
- Gemma-4B-IT: Minimal single-task polling loop (no queues, no ISR notification).
```c
#include <stdio.h>

void app(void)
{
    for(;;) {
        /* read bme, adxl, gps, pir */
        printf("sample\n");
        /* naive delay */
        for (volatile int i = 0; i < 1000000; ++i) {}
    }
}
```

### 5) Embedded Linux Resource Monitor (Sensor Fusion category)
Prompt: "Implement an Embedded Linux resource monitor for your sensor application — track per-thread CPU and memory usage using /proc APIs, and use a mutex-protected shared structure to update statistics. Optionally, display data in real-time using ncurses or a web dashboard."

- H2LooP v0.1 Coder: Per-thread CPU via /proc/[pid]/task/*/stat, memory via /proc/[pid]/smaps, mutex-protected snapshot, simple renderer.
```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <dirent.h>
#include <string.h>
#include <pthread.h>
#include <unistd.h>
#include <sys/types.h>

typedef struct { unsigned long long utime, stime; } thread_cpu_t;
typedef struct { size_t rss_kb; size_t pss_kb; } mem_t;

typedef struct { thread_cpu_t* thr; size_t nthr; mem_t mem; } stats_t;
static stats_t g_stats; static pthread_mutex_t g_mu = PTHREAD_MUTEX_INITIALIZER;

static int parse_tstat(const char* path, thread_cpu_t* out){ FILE* f=fopen(path,"r"); if(!f) return -1; char comm[256], state; unsigned long long ut, st; int pid; // fields per procfs doc
    // pid (1) comm (2) state (3) ... utime (14) stime (15)
    int i=0; int res=0; char buf[4096]; if(!fgets(buf,sizeof buf,f)){ fclose(f); return -1; }
    // naive parse: find last ')' then split fields
    char* rp = strrchr(buf,')'); if(!rp){ fclose(f); return -1; }
    char* p = rp+2; // skip ") "
    // skip fields 3..13
    for(i=3;i<=13;i++){ strtoull(p,&p,10); }
    unsigned long long utime = strtoull(p,&p,10);
    unsigned long long stime = strtoull(p,&p,10);
    out->utime=utime; out->stime=stime; fclose(f); return res;
}

static void read_threads_cpu(pid_t pid, stats_t* s){
    char tdir[128]; snprintf(tdir,sizeof tdir,"/proc/%d/task",pid);
    DIR* d=opendir(tdir); if(!d) return; struct dirent* e; size_t cap=16; size_t n=0;
    thread_cpu_t* arr = (thread_cpu_t*)calloc(cap,sizeof *arr);
    while((e=readdir(d))){ if(e->d_name[0]=='.') continue; char path[256]; snprintf(path,sizeof path,"%s/%s/stat",tdir,e->d_name);
        if(n==cap){ cap*=2; arr=(thread_cpu_t*)realloc(arr,cap*sizeof *arr); }
        if(parse_tstat(path,&arr[n])==0) n++;
    }
    closedir(d);
    s->thr = arr; s->nthr=n;
}

static void read_smaps(pid_t pid, mem_t* m){
    char path[128]; snprintf(path,sizeof path,"/proc/%d/smaps",pid);
    FILE* f=fopen(path,"r"); if(!f) return; char k[64]; size_t v; char unit[8];
    while(fscanf(f,"%63s %zu %7s",k,&v,unit)==3){ if(strcmp(k,"Rss:")==0) m->rss_kb+=v; if(strcmp(k,"Pss:")==0) m->pss_kb+=v; }
    fclose(f);
}

static void* sampler(void* arg){ pid_t pid=getpid(); for(;;){ stats_t s={0}; read_threads_cpu(pid,&s); read_smaps(pid,&s.mem);
        pthread_mutex_lock(&g_mu); // swap into global snapshot
        free(g_stats.thr); g_stats=s; pthread_mutex_unlock(&g_mu);
        usleep(500*1000);
    } return NULL; }

static void* renderer(void* arg){ for(;;){ pthread_mutex_lock(&g_mu); stats_t s=g_stats; pthread_mutex_unlock(&g_mu);
        printf("Threads=%zu RSS=%zuk PSS=%zuk\n", s.nthr, s.mem.rss_kb, s.mem.pss_kb);
        for(size_t i=0;i<s.nthr;i++){ printf("  t[%zu]: ut=%llu st=%llu\n", i, s.thr[i].utime, s.thr[i].stime); }
        sleep(1);
    } return NULL; }

int main(void){ pthread_t ts, tr; pthread_create(&ts,NULL,sampler,NULL); pthread_create(&tr,NULL,renderer,NULL); pthread_join(tr,NULL); return 0; }
```
- GPT OSS 120B: Reads /proc/stat (system-wide) and prints totals; per-thread and mutexing omitted.
```c
#include <stdio.h>
#include <unistd.h>

int main(void)
{
    for (;;) {
        FILE* f = fopen("/proc/stat", "r");
        if (!f) return 1;
        char line[256];
        while (fgets(line, sizeof line, f)) {
            if (line[0]=='c' && line[1]=='p' && line[2]=='u') {
                printf("%s", line);
            }
        }
        fclose(f);
        sleep(1);
    }
}
```
- Gemma-4B-IT: Minimal per-process memory read (rss only) without threading.
```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(void)
{
    pid_t pid = getpid();
    char path[128];
    snprintf(path, sizeof path, "/proc/%d/smaps", pid);
    FILE* f = fopen(path, "r");
    if (!f) return 1;
    char key[64], unit[8];
    size_t v, rss = 0;
    while (fscanf(f, "%63s %zu %7s", key, &v, unit) == 3) {
        if (strcmp(key, "Rss:") == 0) rss += v;
    }
    fclose(f);
    printf("RSS=%zu kB\n", rss);
    return 0;
}
```

### 6) Embedded Linux Resource Monitor (Embedded Linux category)
Prompt: "Implement an Embedded Linux resource monitor for your sensor application — track per-thread CPU and memory usage using /proc APIs, and use a mutex-protected shared structure to update statistics. Optionally, display data in real-time using ncurses or a web dashboard."

- H2LooP v0.1 Coder: Sampler thread + renderer thread with condition variable, mutex-protected snapshot, and signal-safe shutdown.
```c
#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <pthread.h>
#include <unistd.h>
#include <string.h>
#include <dirent.h>
#include <sys/types.h>

typedef struct { unsigned long long utime, stime; } thread_cpu_t;
typedef struct { size_t rss_kb; size_t pss_kb; } mem_t;
typedef struct { thread_cpu_t* thr; size_t nthr; mem_t mem; } stats_t;

static pthread_mutex_t mu = PTHREAD_MUTEX_INITIALIZER;
static pthread_cond_t cv = PTHREAD_COND_INITIALIZER;
static volatile sig_atomic_t g_stop = 0;
static stats_t snap = {0};

static int parse_tstat(const char* path, thread_cpu_t* out){ FILE* f=fopen(path,"r"); if(!f) return -1; char buf[4096]; if(!fgets(buf,sizeof buf,f)){ fclose(f); return -1; } fclose(f);
    char* rp=strrchr(buf,')'); if(!rp) return -1; char* p=rp+2; for(int i=3;i<=13;i++){ strtoull(p,&p,10);} out->utime=strtoull(p,&p,10); out->stime=strtoull(p,&p,10); return 0; }

static void read_threads_cpu(pid_t pid, stats_t* s){
    char tdir[128]; snprintf(tdir,sizeof tdir,"/proc/%d/task",pid); DIR* d=opendir(tdir); if(!d){ s->thr=NULL; s->nthr=0; return; }
    size_t cap=16,n=0; thread_cpu_t* arr=(thread_cpu_t*)calloc(cap,sizeof *arr);
    struct dirent* e; while((e=readdir(d))){ if(e->d_name[0]=='.') continue; char path[256]; snprintf(path,sizeof path,"%s/%s/stat",tdir,e->d_name);
        if(n==cap){ cap*=2; arr=(thread_cpu_t*)realloc(arr,cap*sizeof *arr);} if(parse_tstat(path,&arr[n])==0) n++; }
    closedir(d); s->thr=arr; s->nthr=n;
}

static void read_smaps(pid_t pid, mem_t* m){ char path[128]; snprintf(path,sizeof path,"/proc/%d/smaps",pid); FILE* f=fopen(path,"r"); if(!f) return; char k[64]; size_t v; char unit[8];
    while(fscanf(f,"%63s %zu %7s",k,&v,unit)==3){ if(strcmp(k,"Rss:")==0) m->rss_kb+=v; if(strcmp(k,"Pss:")==0) m->pss_kb+=v; } fclose(f); }

static void stats_free(stats_t* s){ free(s->thr); s->thr=NULL; s->nthr=0; }

static void* sampler(void* arg){ pid_t pid=getpid(); while(!g_stop){ stats_t s={0}; read_threads_cpu(pid,&s); read_smaps(pid,&s.mem);
        pthread_mutex_lock(&mu); stats_free(&snap); snap=s; pthread_cond_signal(&cv); pthread_mutex_unlock(&mu); usleep(250*1000); }
    return NULL; }

static void* renderer(void* arg){ while(!g_stop){ pthread_mutex_lock(&mu); pthread_cond_wait(&cv,&mu); stats_t s=snap; pthread_mutex_unlock(&mu);
        printf("Threads=%zu RSS=%zuk PSS=%zuk\n", s.nthr, s.mem.rss_kb, s.mem.pss_kb);
        for(size_t i=0;i<s.nthr;i++){ printf("  t[%zu]: ut=%llu st=%llu\n", i, s.thr[i].utime, s.thr[i].stime); }
    } return NULL; }

static void on_sigint(int signo){ (void)signo; g_stop=1; pthread_cond_broadcast(&cv); }

int main(void){ signal(SIGINT,on_sigint); pthread_t ts,tr; pthread_create(&ts,NULL,sampler,NULL); pthread_create(&tr,NULL,renderer,NULL); pthread_join(ts,NULL); pthread_join(tr,NULL); stats_free(&snap); return 0; }
```
- GPT OSS 120B: Single-threaded loop that may block rendering while sampling and lacks shutdown coordination.
```c
#include <stdio.h>
#include <unistd.h>
int main(){ for(;;){ FILE* f=fopen("/proc/stat","r"); if(f){ char line[128]; while(fgets(line,sizeof line,f)){ /* print some lines */ } fclose(f);} sleep(1);} }
```
- Gemma-4B-IT: Outline without threading primitives or signal handling.
```c
int main(){ /* TODO: read /proc and print; consider threads and signals */ return 0; }
```



## What it means for Professional Embedded C Developers

H2LooP v0.1 Coder adds measurable value to embedded C workflows by producing code that respects hardware registers, protocol timing, and OS concurrency semantics—closing the gap between “compiles” and “ships.” In day-to-day engineering, this translates to:
- Faster bring-up and fewer lab cycles: register-accurate init (GPIO AF, clock gating, CPOL/CPHA, ACK/NACK) and correct sequencing on SPI/I2C/UART reduce scope for invisible timing bugs.
- Safer boot/update flows: CRC gates, erase-before-write, alignment, and metadata management harden update pipelines and recovery.
- Production-ready concurrency: RTOS task partitioning, ISR-to-task signaling, mutex/condvar patterns, and signal-safe shutdown drive stable behavior under load.
- Higher first-pass success: strong compile reliability with minimal scaffolding accelerates iteration on constrained targets.
- Linux observability that matters: per-thread CPU/memory parsing and snapshotting provides actionable telemetry for debugging and tuning.

Recommended integrations
- Plug H2LooP Knowledge Graph along with our models to instantly index your local codebase in minutes and let the our model generate code as per your vocabulary and taste.
- Generate comprehensive Sequence diagrams off our Mermaid integration to debug what might go wrong faster than ever.
- Pair-program with your HAL/LL: generate driver/bootloader scaffolds and have H2LooP explain register choices and timing assumptions inline.
- Design review copilot: ask H2LooP to audit safety checks (timeouts, integrity, bounds, alignment) and concurrency correctness.
- Standardized templates: let H2LooP produce baseline code for drivers, bootloaders, RTOS tasks, and Linux samplers; you add board-specific deltas.
- Porting assistant: provide target constraints (clock tree, flash geometry, ISR names) to accelerate migration between MCU families.

Conclusion
H2LooP’s domain-guided training and human-in-the-loop evaluation emphasize the details embedded teams rely on—register-level correctness, protocol ordering, integrity and safety checks, and robust concurrency. The resulting solutions achieve higher real-world requirement coverage and strong compile reliability, helping teams deliver faster bring-up, safer field updates, and more predictable deployments across embedded systems developement.
