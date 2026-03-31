# Benchmark Report — System Comparison

**Systems:** H2Loop KG 2.0 · H2Loop KG 1.0 · Naive RAG  
**Dataset:** Questions across markdown, docx, xlsx, xml formats  
**Scoring:** Composite = average of Correctness, Completeness, No-Hallucination, Relevance (each 0–1)

---

## Overall Performance

| System | Correctness | Completeness | No-Hallucination | Relevance | Composite |
|--------|-------------|--------------|-----------------|-----------|-----------|
| H2Loop KG 2.0 | 0.690 | 0.714 | 0.595 | 0.690 | **0.673** |
| H2Loop KG 1.0 (extrapolated) | 0.413 | 0.437 | 0.365 | 0.579 | **0.448** |
| Naive RAG | 0.238 | 0.214 | 0.548 | 0.619 | **0.405** |

> KG 1.0 only supports markdown. Its overall score is extrapolated using the KG 1.0 / KG 2.0 performance ratio 

---

## Performance by Document Format

| Format | KG 2.0 | KG 1.0 | Naive RAG |
|--------|--------|--------|-----------|
| markdown | 0.750 | 0.500 | 0.453 |
| docx | 0.812 | N/A | 0.562 |
| xlsx/xml | 0.464 | N/A | 0.214 |

---

## Markdown Questions

### Query 1: In indirect transmission, what uniquely identifies a transmission request across API calls, and which APIs participate in the lifecycle including confirmation?

**Format:** markdown · **Cross-doc:** No

**Ground Truth:**
> There are 11 SCB blocks: SCB0 (0x40600000), SCB1 (0x40610000), SCB2 (0x40620000), SCB3 (0x40630000), SCB4 (0x40640000), SCB5 (0x40650000), SCB6 (0x40660000), SCB7 (0x40670000), SCB8 (0x40680000), SCB9 (0x40690000), and SCB10 (0x406A0000), spanning the address range 0x40600000–0x406A0000.

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.0 |
| KG 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.000 |
| Naive RAG | 0.5 | 0.5 | 0.5 | 1.0 | 0.625 |

<details>
<summary>KG 2.0 Output</summary>

```
There are 11 SCB blocks in total: SCB0 (0x40600000), SCB1 (0x40610000), SCB2 (0x40620000), SCB3 (0x40630000), SCB4 (0x40640000), SCB5 (0x40650000), SCB6 (0x40660000), SCB7 (0x40670000), SCB8 (0x40680000), SCB9 (0x40690000), and SCB10 (0x406A0000).
```

</details>

<details>
<summary>KG 1.0 Output</summary>

```
The device has 2 SCB (Serial Communication Block) instances—DW0 (0x40288000, CH_STRUCT0–128) and DW1 (0x40298000, CH_STRUCT0–64)—each with 64-byte channel structures containing control, status, descriptor, interrupt, and SRAM registers, configurable for UART, SPI, and I2C.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
Based on the memory mapping provided in the context, there are 11 Serial Communication Blocks (SCB) present. They occupy the address range from 0x40600000 to 0x406aFFFF.

- The base addresses of the SCBs are:
  - SCB 0: 0x40600000
  - SCB 1: 0x40610000
  - SCB 2: 0x40620000
  - SCB 3: 0x40630000
  - SCB 4: 0x40640000
  - SCB 5: 0x40650000
  - SCB 6: 0x40660000
  - SCB 7: 0x40670000
  - SCB 8: 0x40680000
  - SCB 9: 0x40690000
  - SCB 10: 0x406a0000

Each SCB has a size of 64KB (0x10000 bytes), resulting in a contiguous address range from 0x40600000 to 0x406aFFFF.
```

</details>


### Query 2: What initialization dependencies must be satisfied before calling Eth_Init when the controller is on-chip versus off-chip (MACPHY)?

**Format:** md · **Cross-doc:** No

**Ground Truth:**
> On-chip: no other driver services are used, but shared MCU resources must be initialized beforehand. Off-chip (MACPHY): requires other MCAL drivers (e.g., SPI) to be initialized before Eth_Init.

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.000 |
| KG 1.0 | 0.5 | 0.5 | 0.5 | 1.0 | 0.625 |
| Naive RAG | 0.0 | 0.0 | 0.0 | 1.0 | 0.250 |

<details>
<summary>KG 2.0 Output</summary>

```
# Initialization Dependencies for Eth_Init: On-Chip vs. Off-Chip (MACPHY) Controllers

## Overview

The initialization dependencies for the `Eth_Init` function vary depending on whether the Ethernet controller is **on-chip** or **off-chip (MACPHY)**. This distinction affects which external modules and drivers must be initialized before calling `Eth_Init`.

---

## On-Chip Ethernet Controller Dependencies

When the Ethernet controller is **on-chip**, the dependencies are minimal because the controller is integrated into the microcontroller and shares resources directly.

### Key Dependencies:
- **No dependency on other driver services**:
  - The Eth module does **not** use services from other drivers.
- **Digital I/O pin configuration**:
  - Handled by the **Port driver**.
- **MCU module dependency**:
  - The **Mcu module** must configure shared register settings **before** Ethernet module initialization.
- **Clock IP**:
  - Requires clock signals: `fSPB`, `fSRI`, `fLETH100`, and `fLETH`.
- **SRC (Interrupt Router)**:
  - Required for handling transmit and receive interrupts.
- **HSPHY IP (only for SGMII at 1Gbps)**:
  - Required for physical layer configuration when using SGMII interface.

### Initialization Sequence:
1. MCU module initializes shared registers.
2. Port driver configures MII/RMII and MDIO signals (except for SGMII).
3. Clocks are enabled by MCU.
4. SRC is configured for interrupt handling.
5. Call `Eth_Init`.

---

## Off-Chip Ethernet Controller (MACPHY) Dependencies

When the Ethernet controller is **off-chip (MACPHY)**, it typically communicates with the microcontroller via an interface such as **SPI** or **MII**, requiring additional driver dependencies.

### Key Dependencies:
- **MCAL driver dependencies**:
  - Other MCAL drivers (e.g., **SPI**) must be **initialized and running** before calling `Eth_Init`.
- **Sequence compliance**:
  - Initialization sequence must follow guidelines in **SWS ECUStateManager**.
- **Clock IP**:
  - Requires clock signals: `fSPB`, `fSRI`, `fLETH100`, and `fLETH`.
- **PORT Driver**:
  - Configures MII/RMII and MDIO signals routed through port pads.
- **SRC (Interrupt Router)**:
  - Required for interrupt handling.
- **External PHY**:
  - Connected via MDIO interface for configuration and communication.

### Configuration Parameters:
- **`EthCtrlEnableSplitnerface`**:
  - Enables SPI interface processing for MACPHY.
  - If enabled, implies use of SPI protocol (TC6).
- **`EthCtrlConfigSpiConfiguration`**:
  - Configured only if `EthCtrlEnableSplitnerface` is TRUE.
- **`EthCtrlEnableMii`**:
  - Must be TRUE if `EthCtrlEnableSplitnerface` is TRUE.
  - Required for `Eth_WriteMii()` and `Eth_ReadMii()` functions.

### Initialization Sequence:
1. Initialize required MCAL drivers (e.g., SPI).
2. MCU module configures clocks.
3. Port driver configures MII/RMII and MDIO signals.
4. SRC is configured for interrupt handling.
5. Call `Eth_Init`.

---

## Summary of Differences

| Dependency | On-Chip Controller | Off-Chip (MACPHY) Controller |
|------------|--------------------|------------------------------|
| Use of other driver services | ❌ Not used | ✅ Required (e.g., SPI) |
| Port driver | ✅ Required for MII/RMII/MDIO | ✅ Required for MII/RMII/MDIO |
| MCU module | ✅ Required for shared registers | ✅ Required for clocks |
| SPI driver | ❌ Not required | ✅ Required if SPI interface used |
| External PHY | ❌ Integrated | ✅ Connected via MDIO |
| HSPHY IP | ✅ Required only for SGMII | ✅ Required only for SGMII |
| Initialization sequence | MCU → Port → Eth_Init | MCAL drivers → MCU → Port → Eth_Init |

---

## Conclusion

- For **on-chip controllers**, `Eth_Init` requires minimal external dependencies, mainly the MCU and Port drivers.
- For **off-chip (MACPHY) controllers**, `Eth_Init` depends on other MCAL drivers like SPI, and the initialization sequence must follow the ECU State Manager guidelines.
```

</details>

<details>
<summary>KG 1.0 Output</summary>

```
For Eth_Init, on-chip Ethernet controllers are self-contained and require no dependencies on other drivers (except in MACPHY cases), with the Eth driver initializing all necessary hardware resources itself, whereas off-chip MACPHY controllers depend on other MCAL drivers such as SPI that must be initialized first, making the initialization sequence and inter-driver dependencies critical for proper operation.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
### Initialization dependencies before Eth_17_Leth_Init

- On-chip (LETH):
  - No mandatory dependencies. Eth_17_Leth_Init can be called at any time; it only enables the module, selects the PHY interface, and prepares MDIO.
  - PHY initialization is not required before Eth_17_Leth_Init; it may be done before or after Eth_17_Leth_PrepareControllers per the transceiver/interface.
  - The critical dependency is before Eth_17_Leth_SetControllerMode: the external PHY must be initialized and its clock stable at the MAC input.

- Off-chip (MACPHY):
  - Same as above: Eth_17_Leth_Init has no mandatory dependencies; PHY initialization is not required before it.
  - The PHY must be initialized and stable before the first Eth_17_Leth_SetControllerMode call (which completes controller initialization and enables data operations).
```

</details>

---

### Query 3: During indirect transmission, what are the ordered precondition checks performed before enqueuing a frame, and what errors are reported for each failure?

**Format:** md · **Cross-doc:** No

**Ground Truth:**
> 1) Priority match with configured egress queue: ETH_E_UNKNOWN_EGRESS_PRIORITY (continue). 2) Default queue fallback available: if not, return E_NOT_OK. 3) Queue element availability: ETH_E_EGRESS_QUEUE_OCCUPIED and return E_NOT_OK.

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.000 |
| KG 1.0 | 0.5 | 0.5 | 0.5 | 1.0 | 0.625 |
| Naive RAG | 0.0 | 0.0 | 0.0 | 0.0 | 0.000 |

<details>
<summary>KG 2.0 Output</summary>

```
# Indirect Transmission Precondition Checks and Error Reporting

## Ordered Precondition Checks

During indirect transmission using `Eth_ProvideTxBuffer`, the Ethernet driver performs the following precondition checks **in order**:

1. **Priority Matching Check**
   - Verifies if the given priority matches the configured `EthCtrlConfigEgressQueueSortingType` of an `EthCtrlConfigEgressQueue` at the given `CtrlIdx`
   - **Error on failure**: Reports runtime error **ETH_E_UNKNOWN_EGRESS_PRIORITY** and proceeds to next check

2. **Default Queue Enqueue Check**
   - Checks if the Ethernet frame could be enqueued in an `EthCtrlConfigEgressQueue` at the given `CtrlIdx` where no `EthCtrlConfigEgressQueueSortingType` is configured (default queue per [SWS_Eth_CONSTR_00020])
   - **Error on failure**: Returns with **E_NOT_OK** (no specific error code reported)

3. **Queue Element Availability Check**
   - Checks if an element of the identified `EthCtrlConfigEgressQueue` is available
   - **Error on failure**: Reports runtime error **ETH_E_EGRESS_QUEUE_OCCUPIED** and returns with **E_NOT_OK**

## Additional Error Conditions

If all precondition checks pass but no matching egress queue can be identified:
- The Ethernet frame is dropped
- Reports runtime error **ETH_E_NO_MATCHING_EGRESS_QUEUE_IDENTIFIED**

## Development Errors (DET)

The following development errors may also be reported during indirect transmission operations:

- **ETH_17_LETH_E_INV_CTRL_IDX** (0x01): Invalid controller index passed to `Eth_ProvideTxBuffer`
- **ETH_17_LETH_E_UNINIT** (0x02): API service invoked without ETH module/controller initialization
- **ETH_17_LETH_E_PARAM_POINTER** (0x03): Invalid pointer passed to `Eth_ProvideTxBuffer`
- **ETH_17_LETH_E_INV_PARAM** (0x04): Invalid parameter passed to `Eth_ProvideTxBuffer`
```

</details>

<details>
<summary>KG 1.0 Output</summary>

```
In AUTOSAR Ethernet Driver indirect transmission, the driver performs ordered precondition checks including egress queue matching (reporting ETH_E_NO_MATCHING_EGRESS_QUEUE_IDENTIFIED), egress queue availability (ETH_E_EGRESS_QUEUE_OCCUPIED), buffer size validation (ETH_E_EXCEED_EGRESS_QUEUE_ELEMENT), and hardware-supported data transfer validation (ETH_E_HW_SUPPORTED_DATA_TRANSFER_REJECTED) before enqueuing a frame via Eth_ProvideTxBuffer() and transmitting it with Eth_Transmit(), ensuring proper routing, resource availability, size compliance, and hardware capability.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
Based on the provided context, the ordered precondition checks performed before enqueuing a frame for indirect transmission are as follows, along with the corresponding errors reported for each failure:

1.  **Check for Available Transmit Buffer:** The system verifies if a transmit buffer is available for the frame.
    *   **Error on Failure:** `BUFREQ_E_NOT_OK` (Buffer Request Error - Not OK). This is a general error indicating the buffer request could not be satisfied.

2.  **Check for Buffer Size Sufficiency:** The system checks if the requested buffer length does not exceed the configured transmit buffer size.
    *   **Error on Failure:** `BUFREQ_E_OVFL` (Buffer Request Error - Overflow). This indicates the requested buffer length is too large for the available space.

3.  **Check for Valid Data Pointer:** The system ensures the provided data pointer for the frame payload is valid.
    *   **Error on Failure:** `BUFREQ_E_NOT_OK` (Buffer Request Error - Not OK). This error is also used for an invalid data pointer.

4.  **Check for Switch Management Frame Preparation:** If the transmission is managed by a switch, the system verifies that the frame preparation process completes successfully.
    *   **Error on Failure:** `BUFREQ_E_NOT_OK` (Buffer Request Error - Not OK). This error is returned if the switch management frame preparation encounters an issue.

These checks are performed by the `Eth_17_Leth_ProvideTxBuffer()` API, as detailed in the test case "Leth_Tc_CFL_026". The API returns `BUFREQ_OK` if all checks pass, allowing the frame to be enqueued.
```

</details>

---

### Query 4: In indirect transmission, what uniquely identifies a transmission request across API calls, and which APIs participate in the lifecycle including confirmation?

**Format:** markdown · **Cross-doc:** No

**Ground Truth:**
> Identifier: <CtrlIdx, BufIdx> APIs: Eth_ProvideTxBuffer → Eth_Transmit → EthIf_TxConfirmation

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.000 |
| KG 1.0 | 0.5 | 1.0 | 1.0 | 1.0 | 0.875 |
| Naive RAG | 0.5 | 0.5 | 1.0 | 1.0 | 0.750 |

<details>
<summary>KG 2.0 Output</summary>

```
# Indirect Transmission Request Lifecycle and Identification

## Unique Identifier for Transmission Requests

In indirect transmission, a transmission request is uniquely identified across API calls by the combination of:

- **Controller Index (CtrlIdx)**: Identifies the Ethernet controller (range: 0–255)
- **Buffer Index (BufIdx)**: Of type `Eth_BufIdxType`, which includes:
  - The actual buffer index in the lower 16 bits
  - An internal FIFO index reference in the upper 16 bits (when multiple FIFOs are configured)

This tuple (`CtrlIdx`, `BufIdx`) ensures that each transmission request can be tracked and confirmed uniquely throughout its lifecycle.

## APIs Participating in the Lifecycle

### 1. Buffer Provisioning
- **API**: `Eth_ProvideTxBuffer` / `Eth_17_Leth_ProvideTxBuffer()`
- **Purpose**: Reserves a transmission buffer in the egress queue.
- **Output**:
  - `BufIdxPtr`: Pointer to the buffer index (`BufIdx`) which uniquely identifies the reserved egress queue element in combination with `CtrlIdx`.

### 2. Transmission Trigger
- **API**: `Eth_Transmit` / `Eth_17_Leth_Transmit()`
- **Purpose**: Initiates transmission of the Ethernet frame previously reserved.
- **Parameters**:
  - `CtrlIdx`: Controller index
  - `BufIdx`: Buffer index returned from `Eth_ProvideTxBuffer`
  - `TxConfirmation`: Boolean flag indicating whether confirmation is required
  - `FrameType`, `LenByte`, `PhysAddrPtr`: Additional transmission parameters

### 3. Transmission Confirmation
- **API**: `Eth_TxConfirmation` / `Eth_17_Leth_TxConfirmation()`
- **Purpose**: Polling-based confirmation check; releases buffers and invokes upper-layer callback if confirmation was requested.
- **Callback Invoked**:
  - `EthIf_TxConfirmation()` is called with:
    - `BufIdx`: Buffer index identifying the completed transmission
    - `CtrlIdx`: Controller index associated with the transmission

### 4. Interrupt Handling (Optional)
- **API**: `Eth_17_Leth_TxDmaIrqHdlr()`
- **Purpose**: Handles transmission completion via interrupt (only if Tx interrupts are enabled in configuration).
- **Callback Invoked**:
  - `EthIf_TxConfirmation()` is called with:
    - `BufIdx`
    - `CtrlIdx`

## Lifecycle Flow Summary

1. **Reservation**: Upper layer calls `Eth_ProvideTxBuffer()` to reserve a transmit buffer; receives `BufIdx`.
2. **Transmission**: Upper layer calls `Eth_Transmit()` with the same `CtrlIdx` and `BufIdx` to initiate transmission.
3. **Confirmation**:
   - If **Tx interrupts are enabled**: `Eth_17_Leth_TxDmaIrqHdlr()` handles completion and invokes `EthIf_TxConfirmation()`.
   - If **Tx interrupts are disabled**: Upper layer must poll `Eth_TxConfirmation()` to trigger `EthIf_TxConfirmation()`.

## Configuration Dependencies

- **Interrupt Mode**: Whether confirmation is handled via interrupt or polling depends on `EthCtrlConfigEgressEnableInterrupt`.
- **Initialization Sequence**: Transmission APIs require prior initialization via:
  - `Eth_17_Leth_Init()`
  - `Eth_17_Leth_PrepareControllers()`
  - `Eth_17_Leth_SetControllerMode()`

## Contrast with Direct Transmission

- **Direct Transmission API**: `Eth_ImmediateTransmit`
- **Identification**: Uses `TxHandleId` provided by the caller
- **Confirmation API**: `Eth_TxConfirmation` is called with the same `TxHandleId`

---

This synthesis integrates information from all provided documents to present a complete and coherent view of indirect transmission request identification and API lifecycle in the AUTOSAR Ethernet driver.
```

</details>

<details>
<summary>KG 1.0 Output</summary>

```
In AUTOSAR Ethernet indirect transmission, a transmission request is uniquely identified by the combination of CtrlIdx and BufIdxPtr obtained via Eth_ProvideTxBuffer(), after which the buffer is filled and passed to Eth_Transmit() to trigger transmission, and upon completion the driver reports back through EthIf_TxConfirmation() using the same identifiers.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
The unique identifier for an indirect transmission request is the buffer index returned by Eth_ProvideTxBuffer. It is used across Eth_ProvideTxBuffer, Eth_Transmit, and Eth_TxConfirmation (which invokes EthIf_TxConfirmation for confirmation).
```

</details>

---


---

## Structured Format Questions (xlsx/xml)

Questions from xlsx and xml source documents. KG 1.0 does not support these formats.

### Query 5: How many times was 'Leth_Tc_Fn_003' updated as per the revision history of 'Test Data for Eth_17_Leth'

**Format:** xlsx · **Cross-doc:** No

**Ground Truth:**
> Three

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.000 |
| KG 1.0 | — | — | — | — | N/A |
| Naive RAG | 0.0 | 0.0 | 0.0 | 1.0 | 0.250 |

<details>
<summary>KG 2.0 Output</summary>

```
# Updates to 'Leth_Tc_Fn_003' in 'Test Data for Eth_17_Leth'

## Summary

The test case **'Leth_Tc_Fn_003'** was explicitly updated **three times** according to the revision history of the document **'TC4xx_SW_MCAL_TS_Eth_17_Leth.xlsx'** (Document ID: 5921). An additional entry noted the removal of the test case, which is a change in status but not an update per se.

## Revision History Details

- **Version v6.7**
  - **Date**: 1754870400000
  - **Author**: Manikanta Tippana
  - **Changes**:
    - Expectation E4 updated for PHY1 CTRL0 register value (changed from 8 to 0).
    - Typo corrected in Test Procedure.

- **Version v6.4**
  - **Date**: 1754006400000
  - **Author**: Manikanta Tippana
  - **Changes**:
    - Testcase procedure and expectation updated.

- **Version v5.3**
  - **Date**: 1746921600000
  - **Author**: Sreenivasulu Saraswathi
  - **Changes**:
    - Test case updated.

- **Version V1.2**
  - **Date**: 1715644800000
  - **Author**: Sreenivasulu Saraswathi
  - **Changes**:
    - 'Leth_Tc_Fn_003' was **removed**.

## Conclusion

- **Number of Updates**: **3**
- **Note**: One entry refers to the **removal** of the test case, which may or may not be counted as an update depending on context. However, it reflects a change in the test case's lifecycle.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
5 times.

Updates recorded on:
- 2025-05-11 (v5.3)
- 2025-07-30 (v8.0.3)
- 2025-08-01 (v6.4)
- 2025-08-08 (v8.0.8)
- 2025-08-11 (v6.7)
```

</details>

---

### Query 6: For test case Leth_Tc_Fn_002, what is the test objective and what are the expected DUT output parameter values for parameter set P01?

**Format:** xlsx · **Cross-doc:** Yes

**Ground Truth:**
> The objective is to verify that the Ethernet initialization APIs initialize the software and hardware resources of the Ethernet driver according to the user configuration. The expected DUT output parameter values for P01 are: u32l_Test_EthCLC == {0|0|}, u32l_Test_PortEnable == {917518|0|}, u32l_Test_DMA_Int_Status == {0|0|}, u8l_Test_Eth_Ctrl0_EPR == 1,0, u8l_TestEthDmaReset == 0,0, u32l_Test_TXQ_MAP_PORT == {255|255|255|255|}, u32l_Test_RXC_MAP_PORT == {255|255|255|255|}, TotalReportedDets == 0x00, TotalReportedRTEs == 0x00, TotalReportedSE == 0x00, TotalReportedDems == 0x0B.

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 0.0 | 0.5 | 0.625 |
| KG 1.0 | — | — | — | — | N/A |
| Naive RAG | 0.0 | 0.0 | 1.0 | 0.0 | 0.250 |

<details>
<summary>KG 2.0 Output</summary>

```
# Test Case Leth_Tc_Fn_002 Analysis

## Test Objective

The test objective for **Leth_Tc_Fn_002** is to:

> **Verify that the Ethernet initialization APIs initialize the software and hardware resources of the Ethernet driver according to the user configuration.**

This includes validating that:
- Clocks and MAC ports are enabled correctly.
- DMA and PHY interface settings are initialized as configured.
- Controller activation behaves as expected.
- Register mappings (TXQ, RXC, Port Control, Forward Mapping) reflect correct configuration.
- Error reporting and OS interaction during initialization are handled properly.

---

## Expected DUT Output Parameter Values for Parameter Set P01

### Control and Configuration Outputs

| Parameter Name             | Data Type | Condition | Expected Value     |
|----------------------------|-----------|-----------|--------------------|
| `u32l_Test_EthCLC`         | Uint32    | ==        | `{0|0|}`           |
| `u32l_Test_PortEnable`     | Uint32    | ==        | `{917518|0|}`      |
| `u32l_Test_DMA_Int_Status` | Uint32    | ==        | `{0|0|}`           |
| `u8l_Test_Eth_Ctrl0_EPR`   | Byte      | ==        | `1,0`              |
| `u8l_TestEthDmaReset`      | Byte      | ==        | `0,0`              |

### Port Mapping Outputs

| Parameter Name              | Data Type | Condition | Expected Value               |
|-----------------------------|-----------|-----------|------------------------------|
| `u32l_Test_TXQ_MAP_PORT`    | String    | ==        | `{255|255|255|255|}`         |
| `u32l_Test_RXC_MAP_PORT`    | String    | ==        | `{255|255|255|255|}`         |
| `u32l_Test_Ctrl_REG_PORT`   | String    | ==        | `{255|255|255|255|}`         |
| `u32l_Test_Fwd_MAP_PORT`    | String    | ==        | `{255|255|255|255|}`         |

### Test Status and Reporting Outputs

| Parameter Name              | Data Type | Condition | Expected Value                                                                 |
|-----------------------------|-----------|-----------|----------------------------------------------------------------------------------|
| `u8gTestEth_No_User_mode_Flag` | Byte   | ==        | `1`                                                                            |
| `TotalReportedDets`         | Byte      | ==        | `0x00`                                                                         |
| `TotalReportedRTEs`         | Byte      | ==        | `0x00`                                                                         |
| `TotalReportedSE`           | Byte      | ==        | `0x00`                                                                         |
| `TotalReportedDems`         | Byte      | ==        | `0x0B`                                                                         |
| `ReportedDemsList`          | String    | ==        | `0x3E,0x47,0x3E,0x40,0x3F,0x41,0x42,0x45,0x46,0x43,0x44`                      |
| `ReportedStatusList`        | String    | ==        | `0x02,0x00,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02,0x02`                      |

### Input Parameters for Context (P01)

| Parameter Name              | Data Type | Condition | Value for P01     |
|-----------------------------|-----------|-----------|-------------------|
| `u8l_TestEth_NoPorts`       | Byte      | ==        | `1`               |
| `u32l_TestEth_PhyConfig`    | Uint32    | ==        | `0x00000013`      |

---

## Notes
- The test uses **parameter set P01** identified by **AS460_TC49X_C021_P01**.
- The input configuration indicates a single Ethernet port (`u8l_TestEth_NoPorts = 1`) with a specific PHY configuration (`u32l_TestEth_PhyConfig = 0x00000013`).
- All error counts (Development, Runtime, Safety) are expected to be zero.
- DEM events are reported with specific IDs and statuses, indicating successful DEM notification handling.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
Based on the provided context, the details for test case **Leth_Tc_Fn_002** are not available. The context includes information for other test cases (e.g., Leth_Tc_Fn_252, Leth_Tc_Fn_065) and their objectives and expected outputs, but Leth_Tc_Fn_002 is not among them.
```

</details>

---

## Document Format Questions (docx)

Questions from docx source documents. KG 1.0 does not support this format.

### Query 7: What are the three features listed under the ETH_17_LETH static view in the SWA document?

**Format:** docx · **Cross-doc:** No

**Ground Truth:**
> 1. Execution from multiple partitions and in virtualized execution environment, 2. Promiscuous Mode, 3. Accessing internal and external 10BaseT1S configuration register.

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 1.0 | 1.000 |
| KG 1.0 | — | — | — | — | N/A |
| Naive RAG | 0.0 | 0.0 | 0.0 | 1.0 | 0.250 |

<details>
<summary>KG 2.0 Output</summary>

```
# ETH_17_LETH Static View - Features

The following three features are listed under the ETH_17_LETH static view in the SWA document:

## 1. Execution from multiple partitions and in virtualized execution environment
- **Feature ID**: {1DC37C88-A6B1-429c-9988-BB081EB968BB}
- **Parent Requirements**: AU3GM-PRQ-40300, AU3GM-PRQ-40299, {4F734462-DB84-4ccc-821C-B434969A893C}
- **Description**: The Ethernet driver supports execution from multiple partitions and in a virtualized execution environment.
- **Implementation Details**: 
  - The ethernet controller features multiple DMA transmit and receive channels that can be associated with MAC ports
  - DMA channel specific registers are APU protected, allowing the Ethernet driver to support execution in multiple partitions and virtualized environments
  - One or more pairs of DMA TX and RX channels can be allocated to individual partitions or individual executable binaries

## 2. Promiscuous Mode
- **Feature ID**: {76966E53-02A3-4ea4-AC4C-135135081097}
- **Parent Requirement**: AU3GM-PRQ-42193
- **Description**: Promiscuous mode is a mode of operation to pass all the incoming ethernet frames to the upper layer rather than passing only the frames that the controller is specifically programmed to receive.
- **Implementation Details**:
  - Realized by configuring the 'Receive All' feature in the LETH HW
  - When enabled, all ethernet frames are received
  - Configuration provided under 'EthMacPortPromiscuousModeConfig' to select the Rx DMA channel and MTL RxQ for frames that fail MAC port filters

## 3. Accessing internal and external 10BaseT1S configuration register
- **Feature ID**: {EF344138-EE48-4188-A1A0-03641AF073F8}
- **Parent Requirement**: AU3GM-PRQ-42280
- **Description**: The registers related to configuration 10BaseT1S interface are split between the internal LETH HW and external PHY interface. To access these registers using ASR MII APIs, access mode has to be selected in LETH HW.
- **Implementation Details**:
  - External registers are accessed via existing ASR APIs: Eth_17_Leth_WriteMII() and Eth_17_Leth_ReadMII()
  - Requires an API to set the space of registers as internal or external to access the configuration registers of 10BaseT1S interface (Eth_17_Leth_SelectMdioRegSpace())
  - The register space must be set before accessing 10BaseT1S registers via the MII APIs and remains the same until changed by invoking the API again
```

</details>

<details>
<summary>KG 1.0 Output</summary>

```
Based on the provided context from the SWA document (Chunk 3), the three features listed under the ETH_17_LETH static view are:

1.  **Static View**
2.  **Safety View**
3.  **Configuration parameters**

This information is derived from the version history entries, which consistently list these three items together under the "Static View, Safety View" and "Configuration parameters" sections.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
Based on the provided context from the SWA document (Chunk 3), the three features listed under the ETH_17_LETH static view are:

1.  **Static View**
2.  **Safety View**
3.  **Configuration parameters**

This information is derived from the version history entries, which consistently list these three items together under the "Static View, Safety View" and "Configuration parameters" sections.
```

</details>

---

### Query 8: How is promiscuous mode realized in the LETH hardware, and what configuration container controls the Rx DMA channel for frames failing MAC filters?

**Format:** docx · **Cross-doc:** No

**Ground Truth:**
> Promiscuous mode is realized by configuring the 'Receive All' feature in the LETH HW. When enabled, all ethernet frames are received. The configuration container 'EthMacPortPromiscuousModeConfig' is used to select the Rx DMA channel that receives frames which fail the MAC port filters. Frames passing the MAC port filters are received in the intended path as configured.

| System | Correctness | Completeness | No-Halluc | Relevance | Composite |
|--------|-------------|--------------|-----------|-----------|-----------|
| KG 2.0 | 1.0 | 1.0 | 1.0 | 0.5 | 0.875 |
| KG 1.0 | — | — | — | — | N/A |
| Naive RAG | 0.0 | 0.0 | 0.0 | 1.0 | 0.250 |

<details>
<summary>KG 2.0 Output</summary>

```
# Promiscuous Mode and Rx DMA Channel Configuration in LETH Hardware

## Promiscuous Mode Realization

Promiscuous mode in the LETH hardware is realized through multiple mechanisms:

### MAC Port Receive Selection Configuration
Each MAC port is configured with a specific receive selection type that determines how frames are handled:
- **EthMacPortConfig_0** (LETH0_PORT0): `EthMacPortConfigRxSelectionType` = ETH_RXSEL_TYPE_FRAME
- **EthMacPortConfig_1** (LETH1_PORT0): `EthMacPortConfigRxSelectionType` = ETH_RXSEL_TYPE_FRAME
- **EthMacPortConfig_3** (LETH0_PORT1): `EthMacPortConfigRxSelectionType` = ETH_RXSEL_TYPE_FRAME

### Hardware Register Implementation
Two hardware approaches exist for implementing promiscuous mode:

1. **PR bit field** (Port**n**_MAC_Packet_Filter.PR):
   - Changes MAC filter status from FAIL to PASS for unmatched MAC addresses
   - Only affects MAC filter status; VLAN ID filter failures still drop frames
   - Failed frames are received in RxQ0 (default) and cannot be reconfigured

2. **RA bit field** (Port**n**_MAC_Packet_Filter.RA):
   - Receives all Ethernet frames
   - Frames failing MAC/VLAN filters are received with failed status
   - Failed frames can be configured to be received in specific MTL receive queues

### MAC Address Filtering API
The `Eth_UpdatePhysAddrFilter` function controls promiscuous mode behavior:
- Setting MAC address to `FF:FF:FF:FF:FF:FF` completely opens the filter (promiscuous mode)
- Setting MAC address to `00:00:00:00:00:00` restricts filter to controller's unique unicast MAC address and disables promiscuous mode
- If hardware does not support filtering, promiscuous mode must be enabled during initialization

## Rx DMA Channel Configuration for Frames Failing MAC Filters

### Configuration Container
The configuration container **EthMacPortPromiscuousModeConfig** controls the Rx DMA channel routing for frames that fail MAC port filters (MAC/VLANID).

### MAC Port Specific DMA Channel Mapping

#### LETH0_PORT0 (MAC Port 0)
- **EthMacPortConfigReceivePath_0**: 
  - DMA Channel: `/Eth_Leth/Eth/EthDmaConfig_0/EthRxDmaChannel_7`
  - Queue: `/Eth_Leth/Eth/EthConfigSet/EthMacPortConfig_0/EthMacPortConfigRx_0/EthMacPortConfigRxQ_0`
- **EthMacPortConfigReceivePath_1**: 
  - DMA Channel: `/Eth_Leth/Eth/EthDmaConfig_0/EthRxDmaChannel_6`
  - Queue: `/Eth_Leth/Eth/EthConfigSet/EthMacPortConfig_0/EthMacPortConfigRx_0/EthMacPortConfigRxQ_1`

#### LETH1_PORT0 (MAC Port 1)
- **EthMacPortConfigReceivePath_0**: 
  - DMA Channel: `/Eth_Leth/Eth/EthDmaConfig_1/EthRxDmaChannel_0`
  - Queue: `/Eth_Leth/Eth/EthConfigSet/EthMacPortConfig_1/EthMacPortConfigRx_0/EthMacPortConfigRxQ_0`
- **EthMacPortConfigReceivePath_1**: 
  - DMA Channel: `/Eth_Leth/Eth/EthDmaConfig_1/EthRxDmaChannel_1`
  - Queue: `/Eth_Leth/Eth/EthConfigSet/EthMacPortConfig_1/EthMacPortConfigRx_0/EthMacPortConfigRxQ_1`

#### LETH0_PORT1 (MAC Port 3)
- **EthMacPortConfigReceivePath_0**: 
  - DMA Channel: `/Eth_Leth/Eth/EthDmaConfig_0/EthRxDmaChannel_0`
  - Queue: `/Eth_Leth/Eth/EthConfigSet/EthMacPortConfig_3/EthMacPortConfigRx_0/EthMacPortConfigRxQ_0`
- **EthMacPortConfigReceivePath_1**: 
  - DMA Channel: `/Eth_Leth/Eth/EthDmaConfig_0/EthRxDmaChannel_1`
  - Queue: `/Eth_Leth/Eth/EthConfigSet/EthMacPortConfig_3/EthMacPortConfigRx_0/EthMacPortConfigRxQ_1`

### Dedicated Ingress FIFO Configuration for Filter Failures
Specific ingress FIFO configurations handle frames that fail MAC filtering:

- **Controller 1**:
  - Ingress FIFO 0: DMA Channel `/Eth_Leth/Eth/EthDmaConfig_0/EthRxDmaChannel_6`
  - Ingress FIFO 1: DMA Channel `/Eth_Leth/Eth/EthDmaConfig_0/EthRxDmaChannel_7`

These DMA channels are specifically designated for handling frames that fail MAC filtering, allowing separation of filtered vs. unfiltered traffic paths in the receive pipeline.
```

</details>

<details>
<summary>Naive RAG Output</summary>

```
Based on the provided context, the answers to your questions are as follows:

1.  **How is promiscuous mode realized in the LETH hardware?**
    Promiscuous mode is realized by the `Eth_17_Leth_UpdatePhysAddrFilter()` API. When this API is called with the MAC address `FF:FF:FF:FF:FF:FF` and the configuration container `EthMacPortPromiscuousModeConfig` is present (i.e., promiscuous mode support is enabled), the API clears all MAC address filters. This action allows the MAC port to accept all incoming Ethernet frames, effectively enabling promiscuous mode.

2.  **What configuration container controls the Rx DMA channel for frames failing MAC filters?**
    The context does not explicitly name a specific configuration container that controls the Rx DMA channel for frames failing MAC filters. However, the behavior is determined by the MAC port's configuration, specifically the presence or absence of the `EthMacPortPromiscuousModeConfig` container. When promiscuous mode is **not** enabled, the MAC port filters frames based on the configured MAC address list. Frames that do not match any filter are discarded and do not reach the Rx DMA channel. When promiscuous mode **is** enabled (by the method described above), all frames are passed to the Rx DMA channel.
```

</details>

---
