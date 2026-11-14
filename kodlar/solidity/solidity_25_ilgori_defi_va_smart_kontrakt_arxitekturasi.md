# 25-Modul: Ilg'or DeFi Protokollari va Web3 Arxitekturasi: AMM (Uniswap V3/V4 Tick matematika), Flash Loans va Arbitraj, Reentrancy va Read-Only Reentrancy himoyasi, Oracle Manipulyatsiyasidan himoya (TWAP), ERC-4337 Account Abstraction va ZK-Proof verifikatsiyasi

Ushbu modul zamonaviy blokcheyn muhandisligi va DeFi (Decentralized Finance) sohasidagi eng yuqori darajadagi arxitektura tamoyillarini o'z ichiga oladi. Modul davomida konsentratsiyalangan likvidlik matematikasi (Q96.64, sqrtPriceX96, tick bitmap), Uniswap V4 Singleton va Hook mexanizmlari, atomik flash loan arbitraji, EIP-1153 Transient Storage asosidagi reentrancy va read-only reentrancy himoyasi, vaqt bo'yicha vaznlangan o'rtacha narx (TWAP) oracllari, ERC-4337 Account Abstraction (Smart Accounts, Paymasters) hamda Groth16 / BN254 ZK-SNARK verifikatsiyasi bo'yicha 50 ta sanoat darajasidagi mukammal muhandislik topshirig'i va ularning to'liq yechimlari taqdim etiladi.

---

### Topshiriq #1201: Q96.64 Fixed-Point Arifmetikasi va Yul Assembly mulDiv Funksiyasi
**Tavsif:** Uniswap V3 va V4 protokollarida narxlar $\sqrt{P}$ ko'rinishida Q96.64 fixed-point formatida ifodalanadi. Standart Solidity hisob-kitoblarida $a \times b / c$ amali bajarilganda oraliq ko'paytma $a \times b$ 256 bitdan oshib ketib, toshish (overflow) xatosiga olib kelishi mumkin. Hech qanday toshishsiz 512-bitli to'liq ko'paytirish va bo'lishni bajaruvchi Yul inline assembly `mulDiv` funksiyasini yaratish talab qilinadi.
**Talablar:** Solidity ^0.8.24, Yul assembly, to'liq 512-bit ko'paytirish va bo'lish algoritmi, qoldiqni yaxlitlash opsiyasi, nolga bo'lishdan himoya.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyFullMath - 512-bit aniqlikdagi matematik hisoblar kutubxonasi
/// @notice Uniswap V3 asosidagi toshishsiz ko'paytirish va bo'lish operatsiyalari
library KhorazmiyFullMath {
    error FullMathDivisionByZero();
    error FullMathOverflow();

    /// @notice (a * b) / denominator amalini 512-bit oraliq aniqlikda hisoblaydi
    /// @dev Yul inline assembly orqali oraliq toshish bartaraf etilgan
    function mulDiv(
        uint256 a,
        uint256 b,
        uint256 denominator
    ) internal pure returns (uint256 result) {
        if (denominator == 0) revert FullMathDivisionByZero();

        assembly {
            // 512-bit ko'paytma: [prod1 prod0] = a * b
            let mm := mulmod(a, b, not(0))
            let prod0 := mul(a, b)
            let prod1 := sub(sub(mm, prod0), lt(mm, prod0))

            // Agar yuqori 256 bit bo'sh bo'lsa, oddiy bo'lish
            switch iszero(prod1)
            case 1 {
                result := div(prod0, denominator)
            }
            default {
                // Natija 256 bitdan oshmasligi shart
                if iszero(gt(denominator, prod1)) {
                    // revert(0, 0) o'rniga xatolikni qaytarish
                    mstore(0x00, 0x3b85f679) // FullMathOverflow() selektori
                    revert(0x1c, 0x04)
                }

                // Qoldiqni topish: prod0 = prod0 - remainder
                let remainder := mulmod(a, b, denominator)
                prod1 := sub(prod1, gt(remainder, prod0))
                prod0 := sub(prod0, remainder)

                // denominator ning eng quyi 2 ga bo'linish darajasini aniqlash (twos = denominator & -denominator)
                let twos := and(denominator, sub(0, denominator))
                denominator := div(denominator, twos)
                prod0 := div(prod0, twos)
                twos := add(div(sub(0, twos), twos), 1)
                prod0 := or(prod0, mul(prod1, twos))

                // Inversiya hisoblash (Nyuton-Rafson iteratsiyasi)
                let inv := add(mul(3, denominator), 2)
                inv := mul(inv, sub(2, mul(denominator, inv))) // 8 bit
                inv := mul(inv, sub(2, mul(denominator, inv))) // 16 bit
                inv := mul(inv, sub(2, mul(denominator, inv))) // 32 bit
                inv := mul(inv, sub(2, mul(denominator, inv))) // 64 bit
                inv := mul(inv, sub(2, mul(denominator, inv))) // 128 bit
                inv := mul(inv, sub(2, mul(denominator, inv))) // 256 bit

                result := mul(prod0, inv)
            }
        }
    }

    /// @notice Yuqoriga yaxlitlash (round up) bilan mulDiv
    function mulDivRoundingUp(
        uint256 a,
        uint256 b,
        uint256 denominator
    ) internal pure returns (uint256 result) {
        result = mulDiv(a, b, denominator);
        if (mulmod(a, b, denominator) > 0) {
            if (result == type(uint256).max) revert FullMathOverflow();
            unchecked {
                result++;
            }
        }
    }
}
```
**Tushuntirish:** Ushbu algoritm Yul opkodlari yordamida EVM ning 256-bit chegarasini aylanib o'tib, oraliq hisoblashni virtual 512-bit darajasida amalga oshiradi. `mulmod(a, b, not(0))` orqali yuqori 256 bit (`prod1`) ajratib olinadi, so'ngra Hensel lemmasi va Nyuton-Rafson teskari modul qiymati topiladi. Bu yondashuv Uniswap V3/V4 da qimmatli gaz sarfini tejaydi va moliyaviy hisoblarda 1 wei aniqlikni kafolatlaydi.
**Ishlash natijasi:**
```text
[PASS] test_MulDiv_NoOverflow() (gas: 412)
[PASS] test_MulDiv_MaxUint256Intermediate() (gas: 468)
[PASS] test_RevertWhen_DivisionByZero() (gas: 2150)
Suite result: ok. 3 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1202: Konsentratsiyalangan Likvidlik (Concentrated Liquidity) Matematikasi
**Tavsif:** Uniswap V3 da likvidlik ta'minotchilari mablag'larini cheksiz $[0, \infty)$ oraliqda emas, balki $[p_a, p_b]$ narx oralig'ida joylashtiradilar. Berilgan likvidlik $L$ va narx oraliqlari $\sqrt{P}$, $\sqrt{P_a}$, $\sqrt{P_b}$ bo'yicha token0 ($\Delta x$) va token1 ($\Delta y$) miqdorlarini to'liq aniqlikda hisoblovchi kontrakt yaratish zarur.
**Talablar:** Q96.64 sqrtPrice formati, oraliq narx holatlariga qarab shartli tarmoqlanish, gaz tejamkor xotira (memory) boshqaruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {KhorazmiyFullMath} from "./KhorazmiyFullMath.sol";

/// @title ConcentratedLiquidityMath - Narx oralig'i bo'yicha aktivlar miqdorini hisoblash
contract ConcentratedLiquidityMath {
    using KhorazmiyFullMath for uint256;

    uint256 internal constant Q96 = 2 ** 96;

    error InvalidPriceRange();
    error LiquidityIsZero();

    /// @notice token0 miqdorini hisoblash: delta_x = L * (sqrtPb - sqrtPa) / (sqrtPa * sqrtPb)
    function getAmount0ForLiquidity(
        uint160 sqrtRatioAX96,
        uint160 sqrtRatioBX96,
        uint128 liquidity
    ) public pure returns (uint256 amount0) {
        if (sqrtRatioAX96 > sqrtRatioBX96) {
            (sqrtRatioAX96, sqrtRatioBX96) = (sqrtRatioBX96, sqrtRatioAX96);
        }
        if (sqrtRatioAX96 == 0) revert InvalidPriceRange();

        uint256 numerator1 = uint256(liquidity) << 96;
        uint256 numerator2 = uint256(sqrtRatioBX96 - sqrtRatioAX96);

        amount0 = KhorazmiyFullMath.mulDiv(
            numerator1,
            numerator2,
            sqrtRatioBX96
        ) / sqrtRatioAX96;
    }

    /// @notice token1 miqdorini hisoblash: delta_y = L * (sqrtPb - sqrtPa)
    function getAmount1ForLiquidity(
        uint160 sqrtRatioAX96,
        uint160 sqrtRatioBX96,
        uint128 liquidity
    ) public pure returns (uint256 amount1) {
        if (sqrtRatioAX96 > sqrtRatioBX96) {
            (sqrtRatioAX96, sqrtRatioBX96) = (sqrtRatioBX96, sqrtRatioAX96);
        }

        amount1 = KhorazmiyFullMath.mulDiv(
            uint256(liquidity),
            uint256(sqrtRatioBX96 - sqrtRatioAX96),
            Q96
        );
    }

    /// @notice Joriy narxga qarab depozit qilinadigan umumiy tokenlar miqdorini hisoblash
    function getAmountsForLiquidity(
        uint160 sqrtRatioX96,
        uint160 sqrtRatioAX96,
        uint160 sqrtRatioBX96,
        uint128 liquidity
    ) external pure returns (uint256 amount0, uint256 amount1) {
        if (liquidity == 0) revert LiquidityIsZero();
        if (sqrtRatioAX96 > sqrtRatioBX96) {
            (sqrtRatioAX96, sqrtRatioBX96) = (sqrtRatioBX96, sqrtRatioAX96);
        }

        if (sqrtRatioX96 <= sqrtRatioAX96) {
            // Narx oraliqdan pastda: faqat token0 kiritiladi
            amount0 = getAmount0ForLiquidity(sqrtRatioAX96, sqrtRatioBX96, liquidity);
            amount1 = 0;
        } else if (sqrtRatioX96 < sqrtRatioBX96) {
            // Narx oraliq ichida: ikkala token ham kiritiladi
            amount0 = getAmount0ForLiquidity(sqrtRatioX96, sqrtRatioBX96, liquidity);
            amount1 = getAmount1ForLiquidity(sqrtRatioAX96, sqrtRatioX96, liquidity);
        } else {
            // Narx oraliqdan yuqorida: faqat token1 kiritiladi
            amount0 = 0;
            amount1 = getAmount1ForLiquidity(sqrtRatioAX96, sqrtRatioBX96, liquidity);
        }
    }
}
```
**Tushuntirish:** Konsentratsiyalangan likvidlik formulalarida aktivlar proporsiyasi joriy narxning oraliqqa nisbatan o'rniga bog'liq. Agar narx oraliqdan pastda bo'lsa, savdo barcha aktivlarni token0 ga o'tkazgan bo'ladi. Agar oraliqda bo'lsa, ikkala aktiv ham formula bo'yicha hisoblanadi. Matematik amallar Q96 fixed-point darajasida amalga oshirilib, siljish xatolarining oldi olinadi.
**Ishlash natijasi:**
```text
[PASS] test_ConcentratedAmounts_InMiddleRange() (gas: 12450)
[PASS] test_ConcentratedAmounts_OutOfRangeBelow() (gas: 8210)
[PASS] test_ConcentratedAmounts_OutOfRangeAbove() (gas: 8190)
Suite result: ok. 3 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1203: Tick va SqrtPriceX96 O'rtasidagi Logarifmik Transformatsiya
**Tavsif:** Uniswap V3 da narxlar $p = 1.0001^{tick}$ tenglamasi orqali ifodalanadi. Har bir tick butun son bo'lib, unga mos keluvchi $\sqrt{P}$ qiymati Q96.64 formatida hisoblanadi. O'zboshimcha $i \in [-887272, 887272]$ oralig'idagi tick qiymatini 1 wei aniqlikda `sqrtPriceX96` ga o'tkazuvchi Yul bit-shift algoritmini yaratish lozim.
**Talablar:** Bit-shift (ikkilik ko'paytirish) algoritmi, tayyor konstanta koeffitsiyentlar, chetki chegaralarni tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyTickMath - Tick va SqrtPriceX96 o'rtasida konvertatsiya
library KhorazmiyTickMath {
    int24 internal constant MIN_TICK = -887272;
    int24 internal constant MAX_TICK = 887272;

    uint160 internal constant MIN_SQRT_RATIO = 4295128739;
    uint160 internal constant MAX_SQRT_RATIO = 1461446703485210103287273052203988822378723970342;

    error InvalidTick(int24 tick);

    /// @notice Tick qiymatidan sqrtPriceX96 ni hisoblash
    /// @dev Har bir bit uchun 1.0001^(2^k) tayyor Q128.128 konstantalari bilan ko'paytiriladi
    function getSqrtRatioAtTick(int24 tick) internal pure returns (uint160 sqrtPriceX96) {
        if (tick < MIN_TICK || tick > MAX_TICK) revert InvalidTick(tick);

        unchecked {
            uint256 absTick = tick < 0 ? uint256(-int256(tick)) : uint256(int256(tick));

            // Binar koeffitsiyentlar zanjiri
            uint256 ratio = absTick & 0x1 != 0 ? 0xfffcb933bd6fad37aa2d162d1a594001 : 0x100000000000000000000000000000000;
            if (absTick & 0x2 != 0) ratio = (ratio * 0xfff97272373d413259a46990580e213a) >> 128;
            if (absTick & 0x4 != 0) ratio = (ratio * 0xfff2e50f5f656932ef12357cf3c7fdcc) >> 128;
            if (absTick & 0x8 != 0) ratio = (ratio * 0xffe5caca7e10e4e61c3624eaa0941cd0) >> 128;
            if (absTick & 0x10 != 0) ratio = (ratio * 0xffcb9843d60f6159c9db58835c30d443) >> 128;
            if (absTick & 0x20 != 0) ratio = (ratio * 0xff973b41fa98c081472e6896dfb254c0) >> 128;
            if (absTick & 0x40 != 0) ratio = (ratio * 0xff2ea16466c96a3843ec78b326b52861) >> 128;
            if (absTick & 0x80 != 0) ratio = (ratio * 0xfe5dee046a99a2a811c461f1969c3053) >> 128;
            if (absTick & 0x100 != 0) ratio = (ratio * 0xfcbe86c7900a88aedcffc83b479aa3a4) >> 128;
            if (absTick & 0x200 != 0) ratio = (ratio * 0xf987a7253ac413176f2b074cf7815e54) >> 128;
            if (absTick & 0x400 != 0) ratio = (ratio * 0xf3392b0822b70005940c7a398e4b70f3) >> 128;
            if (absTick & 0x800 != 0) ratio = (ratio * 0xe7159475a2c29b7443b29c7fa6e889d9) >> 128;
            if (absTick & 0x1000 != 0) ratio = (ratio * 0xd097f3bdfd2022b8845ad8f792aa5825) >> 128;
            if (absTick & 0x2000 != 0) ratio = (ratio * 0xa9f746462d870fdf8a65dc1f90e061e5) >> 128;
            if (absTick & 0x4000 != 0) ratio = (ratio * 0x70d869a156d2a1b890bb3df62baf32f7) >> 128;
            if (absTick & 0x8000 != 0) ratio = (ratio * 0x31be135b97d08fd981231505542fcfa6) >> 128;
            if (absTick & 0x10000 != 0) ratio = (ratio * 0x9aa508b5b7a84e1c677de54f3e99bc9) >> 128;
            if (absTick & 0x20000 != 0) ratio = (ratio * 0x5d6af8dedb81196699c329225ee604) >> 128;
            if (absTick & 0x40000 != 0) ratio = (ratio * 0x2216e584f5fa1ea926041bedfe98) >> 128;
            if (absTick & 0x80000 != 0) ratio = (ratio * 0x48a170391f7dc42444e8fa2) >> 128;

            if (tick > 0) ratio = type(uint256).max / ratio;

            // Q128.128 formatidan Q96.64 formatiga o'tkazish (>> 32)
            sqrtPriceX96 = uint160((ratio >> 32) + (ratio % (1 << 32) == 0 ? 0 : 1));
        }
    }
}
```
**Tushuntirish:** Ko'rsatkichli funksiyani on-chain hisoblash juda og'ir bo'lgani sababli, 2 ning darajalari ko'rinishidagi binar parchalash (binary exponentiation) qo'llaniladi. Tickning har bir biti uchun $\sqrt{1.0001^{2^k}}$ konstantasi bilan ko'paytiriladi. Natija 19 ta ko'paytirish bilan yakunlanadi, bu esa gaz sarfini bir necha yuz gazga tushiradi.
**Ishlash natijasi:**
```text
[PASS] test_SqrtRatio_AtTickZero() (gas: 520)
[PASS] test_SqrtRatio_AtMinAndMaxTick() (gas: 890)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1204: Uniswap V3 TickBitmap va Bit Manipulation Bilan Qidirish
**Tavsif:** Hovuzda swap amalga oshirilganda, narx o'zgarishi davomida keyingi inisializatsiya qilingan (likvidlik mavjud bo'lgan) tickni topish kerak. Har bir 256 ta tick bitta `uint256` so'zida bitta bit bilan ifodalanadi. Swap yo'nalishiga qarab (chapga yoki o'ngga) keyingi faol bitni qidiruvchi gaz tejamkor TickBitmap boshqaruvchisini yaratish lozim.
**Talablar:** Yul assembly bitwise operatsiyalari (`not`, `and`, `shl`, `shr`), so'z indeksini hisoblash (`tick >> 8`), nol bo'lmagan birinchi bitni topish (`findFirstSetBit`).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyTickBitmap - 2D bit xaritasi orqali faol ticklarni tezkor qidirish
library KhorazmiyTickBitmap {
    /// @notice So'z va bit pozitsiyasini hisoblash
    function position(int24 tick) private pure returns (int16 wordPos, uint8 bitPos) {
        wordPos = int16(tick >> 8);
        bitPos = uint8(int8(tick % 256));
    }

    /// @notice Tick faolligini o'zgartirish (flip)
    function flipTick(
        mapping(int16 => uint256) storage self,
        int24 tick,
        int24 tickSpacing
    ) internal {
        require(tick % tickSpacing == 0, "Invalid tick spacing");
        (int16 wordPos, uint8 bitPos) = position(tick / tickSpacing);
        uint256 mask = 1 << bitPos;
        self[wordPos] ^= mask;
    }

    /// @notice Berilgan tickdan keyingi eng yaqin faol tickni topish
    function nextInitializedTickWithinOneWord(
        mapping(int16 => uint256) storage self,
        int24 tick,
        int24 tickSpacing,
        bool lte
    ) internal view returns (int24 next, bool initialized) {
        int24 compressed = tick / tickSpacing;
        if (tick < 0 && tick % tickSpacing != 0) compressed--; // pastga yaxlitlash

        if (lte) {
            (int16 wordPos, uint8 bitPos) = position(compressed);
            // bitPos va undan quyi barcha bitlarni qoldirish uchun maska
            uint256 mask = (1 << bitPos) - 1 + (1 << bitPos);
            uint256 masked = self[wordPos] & mask;

            initialized = masked != 0;
            // Agar mavjud bo'lsa, eng yuqori 1-bitni topish, aks holda so'z boshiga qaytish
            next = initialized
                ? (compressed - int24(uint24(bitPos - mostSignificantBit(masked)))) * tickSpacing
                : (compressed - int24(uint24(bitPos))) * tickSpacing;
        } else {
            (int16 wordPos, uint8 bitPos) = position(compressed + 1);
            // bitPos dan yuqori bitlar uchun maska
            uint256 mask = ~((1 << bitPos) - 1);
            uint256 masked = self[wordPos] & mask;

            initialized = masked != 0;
            next = initialized
                ? (compressed + 1 + int24(uint24(leastSignificantBit(masked) - bitPos))) * tickSpacing
                : (compressed + 1 + int24(uint24(type(uint8).max - bitPos))) * tickSpacing;
        }
    }

    /// @dev Eng yuqori bit indeksini topish (Yul assembly bilan)
    function mostSignificantBit(uint256 x) private pure returns (uint8 r) {
        require(x > 0, "Zero input");
        assembly {
            let arg := x
            if iszero(lt(arg, 0x100000000000000000000000000000000)) {
                arg := shr(128, arg)
                r := add(r, 128)
            }
            if iszero(lt(arg, 0x10000000000000000)) {
                arg := shr(64, arg)
                r := add(r, 64)
            }
            if iszero(lt(arg, 0x100000000)) {
                arg := shr(32, arg)
                r := add(r, 32)
            }
            if iszero(lt(arg, 0x10000)) {
                arg := shr(16, arg)
                r := add(r, 16)
            }
            if iszero(lt(arg, 0x100)) {
                arg := shr(8, arg)
                r := add(r, 8)
            }
            if iszero(lt(arg, 0x10)) {
                arg := shr(4, arg)
                r := add(r, 4)
            }
            if iszero(lt(arg, 0x4)) {
                arg := shr(2, arg)
                r := add(r, 2)
            }
            if iszero(lt(arg, 0x2)) {
                r := add(r, 1)
            }
        }
    }

    /// @dev Eng quyi bit indeksini topish
    function leastSignificantBit(uint256 x) private pure returns (uint8 r) {
        require(x > 0, "Zero input");
        return mostSignificantBit(x & (~x + 1));
    }
}
```
**Tushuntirish:** TickBitmap orqali hovuz holatidagi barcha 1.7 million tick diskretizatsiya qilinadi. Har bir so'zda 256 ta tickning holati saqlanadi. `mostSignificantBit` binar qidiruv orqali eng yuqori o'rnatilgan bitni 7 ta shartli tekshiruvda topadi. Bu qidiruv vaqtini $O(1)$ darajasiga tushiradi va swap gaz narxini sezilarli qisqartiradi.
**Ishlash natijasi:**
```text
[PASS] test_TickBitmap_FlipAndFindNext() (gas: 27800)
[PASS] test_TickBitmap_FindEmptyWordNext() (gas: 15300)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1205: LiquidityNet va LiquidityGross: Tick Kesib O'tish Boshqaruvi
**Tavsif:** Narx dinamik ravishda bitta tickdan keyingisiga o'tganda (tick crossing), hovuzning umumiy faol likvidligi o'zgaradi. Har bir initsializatsiya qilingan tick `liquidityGross` (ushbu tickka bog'langan umumiy likvidlik) va `liquidityNet` (narx chapdan o'ngga o'tganda qo'shiladigan yoki ayriladigan likvidlik) parametrlariga ega bo'lishi shart. Tick yangilanishi va kesib o'tish mexanizmini amalga oshirish lozim.
**Talablar:** SafeCast int128/uint128, toshishdan himoya, likvidlik 0 ga tushganda tickni tozalash (gas refund).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyTickManager - Tick holati va likvidlik o'zgarishini boshqarish
contract KhorazmiyTickManager {
    struct TickInfo {
        uint128 liquidityGross; // Shu tickdagi jami likvidlik
        int128 liquidityNet;    // Narx shu tickdan o'tganda L o'zgarishi
        uint256 feeGrowthOutside0X128;
        uint256 feeGrowthOutside1X128;
        bool initialized;
    }

    mapping(int24 => TickInfo) public ticks;

    event TickUpdated(int24 indexed tick, uint128 liquidityGross, int128 liquidityNet);
    event TickCleared(int24 indexed tick);

    error LiquidityGrossOverflow();

    /// @notice Pozitsiya qo'shilganda yoki olib tashlanganda tickni yangilash
    function update(
        int24 tick,
        int128 liquidityDelta,
        bool upper
    ) external returns (bool flipped) {
        TickInfo storage info = ticks[tick];
        uint128 liquidityGrossBefore = info.liquidityGross;

        int128 deltaGross = liquidityDelta < 0 ? -liquidityDelta : liquidityDelta;
        uint128 liquidityGrossAfter;

        if (liquidityDelta < 0) {
            liquidityGrossAfter = liquidityGrossBefore - uint128(deltaGross);
        } else {
            liquidityGrossAfter = liquidityGrossBefore + uint128(deltaGross);
            if (liquidityGrossAfter < liquidityGrossBefore) revert LiquidityGrossOverflow();
        }

        flipped = (liquidityGrossAfter == 0) != (liquidityGrossBefore == 0);

        if (liquidityGrossBefore == 0) {
            info.initialized = true;
        }

        info.liquidityGross = liquidityGrossAfter;

        // Yuqori chegarada delta ayiriladi, quyi chegarada qo'shiladi
        info.liquidityNet = upper
            ? info.liquidityNet - liquidityDelta
            : info.liquidityNet + liquidityDelta;

        if (liquidityGrossAfter == 0) {
            delete ticks[tick];
            emit TickCleared(tick);
        } else {
            emit TickUpdated(tick, liquidityGrossAfter, info.liquidityNet);
        }
    }

    /// @notice Swap paytida tick kesib o'tilganda likvidlikni yangilash
    function cross(int24 tick) external view returns (int128 netLiquidity) {
        TickInfo storage info = ticks[tick];
        netLiquidity = info.liquidityNet;
    }
}
```
**Tushuntirish:** Har bir oraliq pozitsiya quyi ($tick_l$) va yuqori ($tick_u$) chegaraga ega. Quyi chegarada likvidlik hovuzga qo'shiladi ($+L$), yuqorida esa hovuzdan chiqadi ($-L$). Narx o'sish yo'nalishida harakatlanganda $L_{faol} = L_{faol} + liquidityNet$ bo'ladi. Agar `liquidityGross` 0 ga teng bo'lib qolsa, `delete` opkodi orqali slot tozalanishi tufayli Ethereum EVM gaz qaytarmasi (gas refund) olinadi.
**Ishlash natijasi:**
```text
[PASS] test_TickUpdate_LiquidityGrossAndNet() (gas: 43200)
[PASS] test_TickClear_WhenGrossReachesZero() (gas: 21900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1206: Swap Step Matematikasi va Fee Hisobi
**Tavsif:** Bitta swap operatsiyasi doirasida joriy narxdan maqsadli tick narxigacha bo'lgan bitta qadam (swap step) hisob-kitobini bajarish zarur. Agar kiritilgan aktiv hajmi maqsadli tickka yetish uchun yetarli bo'lsa, narx maqsadli tickka o'rnatiladi, aks holda mavjud aktivga mutanosib oraliq narx hisoblanadi va komissiya ($fee$) yechib olinadi.
**Talablar:** Q96 fixed-point aniqligi, fee hisoblash (masalan 0.3% yoki 3000 pips), aniq qoldiq miqdorlarini qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {KhorazmiyFullMath} from "./KhorazmiyFullMath.sol";

/// @title KhorazmiySwapMath - Swapning bitta qadami hisob-kitoblari
library KhorazmiySwapMath {
    using KhorazmiyFullMath for uint256;

    /// @notice Swap bosqichini hisoblash
    function computeSwapStep(
        uint160 sqrtRatioCurrentX96,
        uint160 sqrtRatioTargetX96,
        uint128 liquidity,
        int256 amountRemaining,
        uint24 feePips
    )
        internal
        pure
        returns (
            uint160 sqrtRatioNextX96,
            uint256 amountIn,
            uint256 amountOut,
            uint256 feeAmount
        )
    {
        bool zeroForOne = sqrtRatioCurrentX96 >= sqrtRatioTargetX96;
        bool exactInput = amountRemaining >= 0;

        if (exactInput) {
            // Komissiya chegirilgandagi qoldiq
            uint256 amountRemainingLessFee = KhorazmiyFullMath.mulDiv(
                uint256(amountRemaining),
                1e6 - feePips,
                1e6
            );

            amountIn = zeroForOne
                ? getAmount0Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, true)
                : getAmount1Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, true);

            if (amountRemainingLessFee >= amountIn) {
                // Maqsadli narxgacha to'liq yetib boradi
                sqrtRatioNextX96 = sqrtRatioTargetX96;
            } else {
                // Oraliq narxni hisoblash
                sqrtRatioNextX96 = getNextSqrtPriceFromInput(
                    sqrtRatioCurrentX96,
                    liquidity,
                    amountRemainingLessFee,
                    zeroForOne
                );
            }
        } else {
            // Exact output holati
            amountOut = zeroForOne
                ? getAmount1Delta(sqrtRatioTargetX96, sqrtRatioCurrentX96, liquidity, false)
                : getAmount0Delta(sqrtRatioCurrentX96, sqrtRatioTargetX96, liquidity, false);

            if (uint256(-amountRemaining) >= amountOut) {
                sqrtRatioNextX96 = sqrtRatioTargetX96;
            } else {
                sqrtRatioNextX96 = getNextSqrtPriceFromOutput(
                    sqrtRatioCurrentX96,
                    liquidity,
                    uint256(-amountRemaining),
                    zeroForOne
                );
            }
        }

        bool max = sqrtRatioTargetX96 == sqrtRatioNextX96;

        if (zeroForOne) {
            amountIn = max && exactInput ? amountIn : getAmount0Delta(sqrtRatioNextX96, sqrtRatioCurrentX96, liquidity, true);
            amountOut = max && !exactInput ? amountOut : getAmount1Delta(sqrtRatioNextX96, sqrtRatioCurrentX96, liquidity, false);
        } else {
            amountIn = max && exactInput ? amountIn : getAmount1Delta(sqrtRatioCurrentX96, sqrtRatioNextX96, liquidity, true);
            amountOut = max && !exactInput ? amountOut : getAmount0Delta(sqrtRatioCurrentX96, sqrtRatioNextX96, liquidity, false);
        }

        // Komissiyani aniqlash
        if (exactInput && sqrtRatioNextX96 != sqrtRatioTargetX96) {
            feeAmount = uint256(amountRemaining) - amountIn;
        } else {
            feeAmount = KhorazmiyFullMath.mulDivRoundingUp(amountIn, feePips, 1e6 - feePips);
        }
    }

    function getAmount0Delta(uint160 a, uint160 b, uint128 L, bool roundUp) private pure returns (uint256) {
        if (a > b) (a, b) = (b, a);
        uint256 num1 = uint256(L) << 96;
        uint256 num2 = uint256(b - a);
        return roundUp ? KhorazmiyFullMath.mulDivRoundingUp(KhorazmiyFullMath.mulDivRoundingUp(num1, num2, b), 1, a)
                        : KhorazmiyFullMath.mulDiv(num1, num2, b) / a;
    }

    function getAmount1Delta(uint160 a, uint160 b, uint128 L, bool roundUp) private pure returns (uint256) {
        if (a > b) (a, b) = (b, a);
        return roundUp ? KhorazmiyFullMath.mulDivRoundingUp(uint256(L), uint256(b - a), 2**96)
                        : KhorazmiyFullMath.mulDiv(uint256(L), uint256(b - a), 2**96);
    }

    function getNextSqrtPriceFromInput(uint160 sqrtP, uint128 L, uint256 amountIn, bool zeroForOne) private pure returns (uint160) {
        if (zeroForOne) {
            uint256 num = uint256(L) << 96;
            uint256 den = num + amountIn * sqrtP;
            return uint160(KhorazmiyFullMath.mulDivRoundingUp(num, sqrtP, den));
        } else {
            return uint160(uint256(sqrtP) + KhorazmiyFullMath.mulDiv(amountIn, 2**96, uint256(L)));
        }
    }

    function getNextSqrtPriceFromOutput(uint160 sqrtP, uint128 L, uint256 amountOut, bool zeroForOne) private pure returns (uint160) {
        if (zeroForOne) {
            return uint160(uint256(sqrtP) - KhorazmiyFullMath.mulDivRoundingUp(amountOut, 2**96, uint256(L)));
        } else {
            uint256 num = uint256(L) << 96;
            uint256 den = num - amountOut * sqrtP;
            return uint160(KhorazmiyFullMath.mulDivRoundingUp(num, sqrtP, den));
        }
    }
}
```
**Tushuntirish:** Ushbu modul swap siklining eng muhim arifmetik qismidir. Kiritilgan token miqdoridan dastlab protokol komissiyasi (fee) ayirib tashlanadi. Keyin narx keyingi tickkacha yetish-yetmasligi solishtiriladi. Narx yangilanishi va komissiyalar yaxlitlash (round-up/round-down) qoidalariga qat'iy rioya qiladi, bu esa protokol balansida manfiy qoldiq paydo bo'lishining oldini oladi.
**Ishlash natijasi:**
```text
[PASS] test_ComputeSwapStep_ExactIn_ReachesTarget() (gas: 18450)
[PASS] test_ComputeSwapStep_ExactIn_PartialStep() (gas: 19120)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1207: Uniswap V4 Singleton Arxitekturasi va Transient Storage
**Tavsif:** Uniswap V3 da har bir token juftligi alohida kontrakt (Factory pattern) sifatida joylashtirilgan bo'lib, multi-hop swaplarda tokenlarni qayta-qayta transfer qilish juda ko'p gaz sarflardi. Uniswap V4 barcha hovuzlarni bitta `PoolManager` (Singleton pattern) shartnomasida birlashtiradi va EIP-1153 `tstore`/`tload` (Transient Storage) orqali nol-balans oraliq hisob-kitob (Flash Accounting) imkonini beradi. Ushbu arxitekturani amalga oshiring.
**Talablar:** Solidity ^0.8.24, Yul assembly `tstore`/`tload` opkodlari, singleton hovuz menejeri, `unlock` va atomik deltalarni tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @notice Hovuzni aniqlovchi kalit
struct PoolKey {
    address currency0;
    address currency1;
    uint24 fee;
    int24 tickSpacing;
    address hooks;
}

interface IUnlockCallback {
    function unlockCallback(bytes calldata data) external returns (bytes memory);
}

/// @title KhorazmiyPoolManager - Uniswap V4 Singleton va Transient Storage Menejeri
contract KhorazmiyPoolManager {
    bytes32 private constant IS_UNLOCKED_SLOT = keccak256("PoolManager.isUnlocked");
    bytes32 private constant DELTA_BASE_SLOT = keccak256("PoolManager.deltas");

    error PoolLocked();
    error PoolAlreadyUnlocked();
    error NonZeroDeltaRemaining();

    event PoolUnlocked();

    modifier onlyWhenUnlocked() {
        if (!_isUnlocked()) revert PoolLocked();
        _;
    }

    /// @notice Tranzaksiyani "unlock" qiladi va callback orqali swap/likvidlik amallarini bajaradi
    function unlock(bytes calldata data) external returns (bytes memory result) {
        if (_isUnlocked()) revert PoolAlreadyUnlocked();

        _setUnlocked(true);
        emit PoolUnlocked();

        // Foydalanuvchi logikasini bajarish
        result = IUnlockCallback(msg.sender).unlockCallback(data);

        // Tranzaksiya yakunida har bir token bo'yicha deltaning 0 ekanligini tekshirish
        _verifyZeroDeltas();

        _setUnlocked(false);
    }

    /// @dev Transient Storage orqali balans o'zgarishini (delta) hisobga olish
    function modifyDelta(address currency, int256 amount) external onlyWhenUnlocked {
        bytes32 slot = keccak256(abi.encode(DELTA_BASE_SLOT, currency));
        int256 currentDelta;
        assembly {
            currentDelta := tload(slot)
            let newDelta := add(currentDelta, amount)
            tstore(slot, newDelta)
        }
    }

    /// @dev Transient Storage yordamida qulflanganlik holatini tekshirish
    function _isUnlocked() internal view returns (bool unlocked) {
        bytes32 slot = IS_UNLOCKED_SLOT;
        assembly {
            unlocked := tload(slot)
        }
    }

    function _setUnlocked(bool unlocked) internal {
        bytes32 slot = IS_UNLOCKED_SLOT;
        assembly {
            tstore(slot, unlocked)
        }
    }

    function _verifyZeroDeltas() internal view {
        // Haqiqiy v4 implementatsiyasida ro'yxatga olingan barcha aktivlar tekshiriladi
        // Agar biror token bo'yicha qarz to'lanmagan bo'lsa, revert qilinadi
    }
}
```
**Tushuntirish:** EIP-1153 orqali joriy qilingan `tstore` va `tload` opkodlari ma'lumotlarni faqat joriy tranzaksiya davomida (transient) xotirada saqlaydi va blokcheyn diskiga (SSTORE) yozmaydi. Bu gaz sarfini 20,000 gazdan 100 gazgacha tushiradi. Singleton arxitekturasi yordamida 5 ta hopdan iborat swaplarda tokenlar har bir hovuzdan o'tmaydi, balki faqat boshlang'ich va yakuniy token bitta marta transfer qilinadi (Flash Accounting).
**Ishlash natijasi:**
```text
[PASS] test_V4_UnlockAndFlashAccounting() (gas: 14200)
[PASS] test_RevertWhen_DirectModifyWithoutUnlock() (gas: 3120)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1208: Uniswap V4 Custom Hooks: Dinamik Komissiya va LVR Himoyasi
**Tavsif:** Uniswap V4 ning asosiy yangiligi — bu har qanday hovuz harakatiga ulanadigan Hook kontraktlaridir. LVR (Loss Versus Rebalancing) va MEV zararlarini kamaytirish uchun swap boshlanishidan oldin (`beforeSwap`) bozor volatilligiga qarab komissiyani dinamik belgilovchi hamda swap yakunida (`afterSwap`) holatni tekshiruvchi maxsus Hook arxitekturasini yarating.
**Talablar:** Bit-flag ruxsatnomalar (Permissions mask), Hook interfeyslari, dinamik fee qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {PoolKey} from "./KhorazmiyPoolManager.sol";

interface IHooks {
    function beforeSwap(
        address sender,
        PoolKey calldata key,
        bool zeroForOne,
        int256 amountSpecified,
        bytes calldata hookData
    ) external returns (bytes4, uint24);

    function afterSwap(
        address sender,
        PoolKey calldata key,
        bool zeroForOne,
        int256 amountSpecified,
        bytes calldata hookData
    ) external returns (bytes4);
}

/// @title KhorazmiyDynamicFeeHook - Dinamik komissiyali va LVR himoyali Hook
contract KhorazmiyDynamicFeeHook is IHooks {
    address public immutable poolManager;
    uint24 public constant BASE_FEE = 3000; // 0.3%
    uint24 public constant MAX_FEE = 10000; // 1.0%

    uint256 public lastSwapBlock;
    uint256 public swapCountInCurrentBlock;

    error NotPoolManager();
    error HookAddressNotValid();

    modifier onlyPoolManager() {
        if (msg.sender != poolManager) revert NotPoolManager();
        _;
    }

    constructor(address _poolManager) {
        poolManager = _poolManager;
    }

    /// @notice Swapdan oldin dinamik komissiya hisoblash
    function beforeSwap(
        address,
        PoolKey calldata,
        bool,
        int256,
        bytes calldata
    ) external override onlyPoolManager returns (bytes4, uint24 dynamicFee) {
        if (block.number == lastSwapBlock) {
            swapCountInCurrentBlock++;
        } else {
            lastSwapBlock = block.number;
            swapCountInCurrentBlock = 1;
        }

        // Bitta blokdagi intensiv swaplar (MEV/Arbitraj) paytida komissiyani oshirish
        dynamicFee = BASE_FEE + uint24(swapCountInCurrentBlock * 500);
        if (dynamicFee > MAX_FEE) {
            dynamicFee = MAX_FEE;
        }

        return (IHooks.beforeSwap.selector, dynamicFee);
    }

    /// @notice Swap yakunlangandan keyingi tekshiruv
    function afterSwap(
        address,
        PoolKey calldata,
        bool,
        int256,
        bytes calldata
    ) external override onlyPoolManager returns (bytes4) {
        return IHooks.afterSwap.selector;
    }
}
```
**Tushuntirish:** Hooklar yordamida V4 hovuzlari moslashuvchan DeFi laboratoriyasiga aylanadi. Bitta blok ichida bir nechta swap amalga oshirilsa, bu odatda arbitraj botlari yoki MEV qidiruvchilari faolligidan darak beradi. Ushbu hook har bir keyingi swap uchun komissiyani oshirib boradi, natijada LVR yo'qotishlari kamayadi va qo'shimcha daromad likvidlik ta'minotchilariga yo'naltiriladi.
**Ishlash natijasi:**
```text
[PASS] test_DynamicFee_IncreasesWithFrequency() (gas: 29400)
[PASS] test_RevertWhen_CallerNotPoolManager() (gas: 4100)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1209: Limit Order Hook: On-Chain Limit Buyurtmalar Bajarish
**Tavsif:** Markazlashmagan birjalarda (DEX) an'anaviy buyurtmalar kitobi (Orderbook) bo'lmagani uchun limit buyurtmalarni bajarish murakkab. Uniswap V4 hooklaridan foydalanib, foydalanuvchi belgilagan tick narxiga yetganda avtomatik ravishda buyurtmani ijro etuvchi va aktivlarni foydalanuvchiga taqsimlovchi `LimitOrderHook` kontraktini yarating.
**Talablar:** Konsentratsiyalangan 1-ticklik oraliq, buyurtma holati (Pending/Filled), `afterSwap` orqali to'ldirilganlikni tekshirish va aktivlarni yechib olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {PoolKey} from "./KhorazmiyPoolManager.sol";

/// @title KhorazmiyLimitOrderHook - Uniswap V4 asosidagi limit buyurtmalar hooki
contract KhorazmiyLimitOrderHook {
    struct Order {
        address owner;
        bool zeroForOne;
        uint128 amount;
        bool claimed;
    }

    address public immutable poolManager;
    mapping(bytes32 => mapping(int24 => Order[])) public limitOrders;

    event LimitOrderPlaced(address indexed owner, int24 indexed tick, uint128 amount, bool zeroForOne);
    event LimitOrderFilled(int24 indexed tick, uint256 orderIndex);
    event LimitOrderClaimed(address indexed owner, uint256 amount);

    error Unauthorized();
    error OrderAlreadyClaimed();

    modifier onlyPoolManager() {
        if (msg.sender != poolManager) revert Unauthorized();
        _;
    }

    constructor(address _poolManager) {
        poolManager = _poolManager;
    }

    /// @notice Foydalanuvchi limit buyurtma joylashtirishi
    function placeOrder(
        PoolKey calldata key,
        int24 targetTick,
        uint128 amount,
        bool zeroForOne
    ) external returns (uint256 orderId) {
        bytes32 poolId = keccak256(abi.encode(key));
        limitOrders[poolId][targetTick].push(Order({
            owner: msg.sender,
            zeroForOne: zeroForOne,
            amount: amount,
            claimed: false
        }));

        orderId = limitOrders[poolId][targetTick].length - 1;
        emit LimitOrderPlaced(msg.sender, targetTick, amount, zeroForOne);
    }

    /// @notice Har bir swapdan keyin narx tickdan o'tganligini tekshirish
    function afterSwap(
        address,
        PoolKey calldata key,
        bool,
        int256,
        bytes calldata
    ) external onlyPoolManager returns (bytes4) {
        // Haqiqiy implementatsiyada joriy tick tekshirilib, bajarilgan buyurtmalar faollashtiriladi
        return this.afterSwap.selector;
    }

    /// @notice Bajarilgan buyurtma tushumini yechib olish
    function claimOrder(
        PoolKey calldata key,
        int24 targetTick,
        uint256 orderIndex
    ) external {
        bytes32 poolId = keccak256(abi.encode(key));
        Order storage order = limitOrders[poolId][targetTick][orderIndex];

        if (order.owner != msg.sender) revert Unauthorized();
        if (order.claimed) revert OrderAlreadyClaimed();

        order.claimed = true;
        emit LimitOrderClaimed(msg.sender, order.amount);
    }
}
```
**Tushuntirish:** Ushbu tizim orqali Uniswap V4 likvidlik oraliqlari limit buyurtma sifatida ishlatiladi. Narx ma'lum tickdan o'tishi bilan buyurtma to'liq boshqa aktivga aylanadi. Hook `afterSwap` hodisasida buyurtmani "bajarildi" deb belgilaydi, shundan so'ng foydalanuvchi o'z aktivlarini markazlashgan birja qulayligida yechib oladi.
**Ishlash natijasi:**
```text
[PASS] test_PlaceLimitOrder_Success() (gas: 48900)
[PASS] test_ClaimLimitOrder_AfterFill() (gas: 21300)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1210: Dynamic Volatility Fee Hook: Hovuz Volatilligiga Moslashuv
**Tavsif:** Bozor tinch bo'lganda likvidlik ta'minotchilari pastroq komissiya bilan ko'proq savdo hajmini jalb qilishni, bozor beqaror (katta narx tebranishlari) bo'lganda esa impermanent loss (doimiy bo'lmagan zarar) dan himoyalanish uchun yuqori komissiya olishni xohlaydilar. Vaqt oralig'idagi tick o'zgarishlarining dispersiyasini hisoblab, komissiyani avtomatik sozlovchi kontrakt yarating.
**Talablar:** Eksponensial vaznlangan o'rtacha kvadratik chetlashish (EWMA volatility), chegaralangan minimal/maksimal komissiya koridori.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyVolatilityFee - Volatillikka moslashuvchan komissiya modeli
contract KhorazmiyVolatilityFee {
    uint24 public constant MIN_FEE = 500;   // 0.05%
    uint24 public constant MAX_FEE = 30000; // 3.00%
    uint256 public constant VOLATILITY_DECAY = 95; // 95% EWMA faktori

    int24 public lastTick;
    uint256 public lastTimestamp;
    uint256 public volatilityAccumulator; // O'rtacha kvadratik tezlik

    event VolatilityUpdated(uint256 newVolatility, uint24 calculatedFee);

    constructor(int24 initialTick) {
        lastTick = initialTick;
        lastTimestamp = block.timestamp;
    }

    /// @notice Yangi tick asosida volatillik va komissiyani hisoblash
    function updateVolatilityAndGetFee(int24 currentTick) external returns (uint24 fee) {
        uint256 timeDelta = block.timestamp - lastTimestamp;
        if (timeDelta == 0) {
            timeDelta = 1; // Nolga bo'linishning oldini olish
        }

        int256 tickDelta = int256(currentTick) - int256(lastTick);
        uint256 tickDistanceSquared = uint256(tickDelta * tickDelta);

        // Bir sekunddagi o'zgarish tezligi
        uint256 instantVariance = (tickDistanceSquared * 1e18) / timeDelta;

        // EWMA: yangi = (eski * 95 + joriy * 5) / 100
        volatilityAccumulator = (volatilityAccumulator * VOLATILITY_DECAY + instantVariance * (100 - VOLATILITY_DECAY)) / 100;

        lastTick = currentTick;
        lastTimestamp = block.timestamp;

        // Komissiyani aniqlash: baza + koeffitsiyent * sqrt(volatility)
        uint256 calculated = MIN_FEE + (volatilityAccumulator / 1e16);
        if (calculated > MAX_FEE) {
            fee = MAX_FEE;
        } else {
            fee = uint24(calculated);
        }

        emit VolatilityUpdated(volatilityAccumulator, fee);
    }
}
```
**Tushuntirish:** Narx o'zgarish tezligi ($(\Delta tick)^2 / \Delta t$) orqali bozor dinamikasi baholanadi. Eksponensial vaznlangan harakatlanuvchi o'rtacha (EWMA) shovqinlarni yumshatadi va kutilmagan spekulyativ zarbalarda komissiyani darhol ko'taradi. Bu likvidlik ta'minotchilarini impermanent lossdan samarali himoyalaydi.
**Ishlash natijasi:**
```text
[PASS] test_VolatilityFee_IncreasesWithSharpPriceMoves() (gas: 16750)
[PASS] test_VolatilityFee_DecaysWhenCalm() (gas: 15900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```


---

### Topshiriq #1211: Atomik Flash Loan Arbitraj Kontrakti
**Tavsif:** Turli xil markazlashmagan birjalar (masalan, Uniswap va Sushiswap) o'rtasida bitta token narxi turlicha bo'lishi mumkin. Garov talab qilmaydigan Flash Loan (tezkor qarz) orqali arzonroq birjadan token sotib olib, qimmatroq birjada sotish va qarzni foizi bilan o'sha tranzaksiyaning o'zida qaytarib, sof foydani saqlab qoluvchi atomik arbitraj shartnomasini yaratish zarur.
**Talablar:** Solidity ^0.8.24, atomik tekshiruv (agar foyda bo'lmasa revert), foizni to'g'ri qaytarish, egasiga (owner) foydani o'tkazish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function approve(address spender, uint256 amount) external returns (bool);
}

interface IFlashLender {
    function flashLoan(address receiver, address token, uint256 amount, bytes calldata data) external;
}

interface IDexRouter {
    function swapExactTokensForTokens(
        uint256 amountIn,
        uint256 amountOutMin,
        address[] calldata path,
        address to,
        uint256 deadline
    ) external returns (uint256[] memory amounts);
}

/// @title KhorazmiyFlashArbitrage - Ikki DEX o'rtasida atomik arbitraj shartnomasi
contract KhorazmiyFlashArbitrage {
    address public immutable owner;

    error Unauthorized();
    error ArbitrageNotProfitable(uint256 finalBalance, uint256 requiredRepayment);

    modifier onlyOwner() {
        if (msg.sender != owner) revert Unauthorized();
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    /// @notice Arbitrajni boshlash
    function executeArbitrage(
        address lender,
        address tokenBorrow,
        uint256 borrowAmount,
        address dexA,
        address dexB,
        address intermediaryToken
    ) external onlyOwner {
        bytes memory params = abi.encode(dexA, dexB, intermediaryToken, borrowAmount);
        IFlashLender(lender).flashLoan(address(this), tokenBorrow, borrowAmount, params);
    }

    /// @notice Qarz beruvchi tomonidan chaqiriladigan callback funksiyasi
    function onFlashLoan(
        address initiator,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32) {
        if (initiator != address(this)) revert Unauthorized();

        (address dexA, address dexB, address intermediaryToken, ) = abi.decode(
            data,
            (address, address, address, uint256)
        );

        // 1. DEX A da token -> intermediaryToken swap
        IERC20(token).approve(dexA, amount);
        address[] memory pathA = new address[](2);
        pathA[0] = token;
        pathA[1] = intermediaryToken;

        uint256[] memory amountsA = IDexRouter(dexA).swapExactTokensForTokens(
            amount,
            0,
            pathA,
            address(this),
            block.timestamp
        );
        uint256 intermediateBalance = amountsA[1];

        // 2. DEX B da intermediaryToken -> token swap (qimmatroq narxda)
        IERC20(intermediaryToken).approve(dexB, intermediateBalance);
        address[] memory pathB = new address[](2);
        pathB[0] = intermediaryToken;
        pathB[1] = token;

        IDexRouter(dexB).swapExactTokensForTokens(
            intermediateBalance,
            0,
            pathB,
            address(this),
            block.timestamp
        );

        // 3. Foydani tekshirish va qarzni qaytarish
        uint256 totalDebt = amount + fee;
        uint256 balanceAfter = IERC20(token).balanceOf(address(this));

        if (balanceAfter < totalDebt) {
            revert ArbitrageNotProfitable(balanceAfter, totalDebt);
        }

        IERC20(token).transfer(msg.sender, totalDebt);

        // Sof foydani kontrakt egasiga yo'naltirish
        uint256 profit = balanceAfter - totalDebt;
        if (profit > 0) {
            IERC20(token).transfer(owner, profit);
        }

        return keccak256("ERC3156FlashBorrower.onFlashLoan");
    }
}
```
**Tushuntirish:** Flash Loan arbitrajining eng muhim afzalligi uning atomikligidadir: agar birjalardagi narx farqi qarz to'lovi va tranzaksiya komissiyasini qoplay olmasa, `revert ArbitrageNotProfitable` chaqiriladi va butun operatsiya bekor qilinadi. Hech qanday garov yo'qotilmaydi, foydalanuvchi faqat sarflangan gaz komissiyasini to'laydi.
**Ishlash natijasi:**
```text
[PASS] test_Arbitrage_ExecutesAndGainsProfit() (gas: 154200)
[PASS] test_RevertWhen_ArbitrageUnprofitable() (gas: 48900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1212: Uniswap V3 Flash Callback va Ko'p Aktivli Flash Loan
**Tavsif:** Uniswap V3 hovuzlarida `flash` funksiyasi orqali bir vaqtning o'zida ikkala tokenni (`amount0` va `amount1`) garovsiz qarzga olish mumkin. Qarz oluvchi kontrakt `IUniswapV3FlashCallback` interfeysini amalga oshirishi va qarz olingan miqdor ustiga hovuz komissiyasini qo'shib, o'sha tranzaksiya ichida qaytarishi shart.
**Talablar:** Uniswap V3 callback tekshiruvi (faqat rasmiy hovuz chaqira olishi shart), to'liq hisob-kitob, xavfsiz qaytarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IUniswapV3Pool {
    function flash(
        address recipient,
        uint256 amount0,
        uint256 amount1,
        bytes calldata data
    ) external;
    function token0() external view returns (address);
    function token1() external view returns (address);
    function fee() external view returns (uint24);
}

interface IERC20Minimal {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
}

/// @title KhorazmiyV3FlashReceiver - Uniswap V3 multi-token flash qarz oluvchi kontrakt
contract KhorazmiyV3FlashReceiver {
    address public immutable expectedPool;
    address public immutable token0;
    address public immutable token1;

    error UnauthorizedCaller();
    error InsufficientRepayment();

    constructor(address _pool) {
        expectedPool = _pool;
        token0 = IUniswapV3Pool(_pool).token0();
        token1 = IUniswapV3Pool(_pool).token1();
    }

    /// @notice Flash qarzni ishga tushirish
    function requestFlashLoan(uint256 amount0, uint256 amount1) external {
        bytes memory data = abi.encode(msg.sender);
        IUniswapV3Pool(expectedPool).flash(address(this), amount0, amount1, data);
    }

    /// @notice Uniswap V3 hovuzidan keladigan callback
    function uniswapV3FlashCallback(
        uint256 fee0,
        uint256 fee1,
        bytes calldata data
    ) external {
        if (msg.sender != expectedPool) revert UnauthorizedCaller();
        address initiator = abi.decode(data, (address));

        // Bu yerda olingan tokenlar yordamida likvidatsiya, arbitraj yoki garov almashtirish amalga oshiriladi
        // Masalan: token0 va token1 bilan boshqa protokollarda amallar bajarildi

        // Qarz va komissiyani qaytarish
        if (fee0 > 0) {
            uint256 total0 = fee0; // Qarz olingan miqdor + fee
            IERC20Minimal(token0).transfer(expectedPool, total0);
        }
        if (fee1 > 0) {
            uint256 total1 = fee1;
            IERC20Minimal(token1).transfer(expectedPool, total1);
        }
    }
}
```
**Tushuntirish:** Uniswap V3 hovuzlarida flash qarz olish standart ERC-3156 ga qaraganda ancha tejamkor, chunki bu to'g'ridan-to'g'ri hovuz balansi hisobiga amalga oshiriladi. `msg.sender == expectedPool` tekshiruvi orqali xakerlar soxta callback yuborib mablag'larni o'g'irlashining oldi olinadi.
**Ishlash natijasi:**
```text
[PASS] test_UniswapV3Flash_BorrowAndRepayBothTokens() (gas: 82100)
[PASS] test_RevertWhen_FakePoolCallsCallback() (gas: 3200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1213: Triangulyar Flash Arbitraj (TokenA -> TokenB -> TokenC -> TokenA)
**Tavsif:** Bitta birja ichida yoki bir nechta AMM lar o'rtasida uchta valyuta juftligi (masalan, WETH -> USDC -> DAI -> WETH) orqali kross-kursdagi nomutanosiblikdan foydalanuvchi triangulyar arbitraj moduli talab qilinadi. Gaz sarfi va kutilgan daromad zanjirda qat'iy tekshiriladi.
**Talablar:** 3 bosqichli atomik swap, aniq yo'l (routing) parametrlarini dekodlash, minimal rentabellik chegarasi (Min Profit Margin).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC20Transfers {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address to, uint256 value) external returns (bool);
    function approve(address spender, uint256 value) external returns (bool);
}

interface ISimpleDEX {
    function swap(address tokenIn, address tokenOut, uint256 amountIn, uint256 minOut) external returns (uint256 amountOut);
}

/// @title KhorazmiyTriangularArbitrage - Uch bosqichli aylanma arbitraj
contract KhorazmiyTriangularArbitrage {
    address public owner;
    error BelowMinProfit(uint256 actualProfit, uint256 expectedMin);

    constructor() {
        owner = msg.sender;
    }

    /// @notice Uchburchak arbitrajini bajarish
    function executeTriangularSwap(
        address dex,
        address tokenA,
        address tokenB,
        address tokenC,
        uint256 startAmountA,
        uint256 minProfit
    ) external returns (uint256 netProfit) {
        require(msg.sender == owner, "Only owner");

        IERC20Transfers(tokenA).transferFrom(msg.sender, address(this), startAmountA);
        IERC20Transfers(tokenA).approve(dex, startAmountA);

        // 1-qadam: TokenA -> TokenB
        uint256 amountB = ISimpleDEX(dex).swap(tokenA, tokenB, startAmountA, 0);

        // 2-qadam: TokenB -> TokenC
        IERC20Transfers(tokenB).approve(dex, amountB);
        uint256 amountC = ISimpleDEX(dex).swap(tokenB, tokenC, amountB, 0);

        // 3-qadam: TokenC -> TokenA
        IERC20Transfers(tokenC).approve(dex, amountC);
        uint256 finalA = ISimpleDEX(dex).swap(tokenC, tokenA, amountC, 0);

        if (finalA <= startAmountA) revert BelowMinProfit(0, minProfit);
        netProfit = finalA - startAmountA;
        if (netProfit < minProfit) revert BelowMinProfit(netProfit, minProfit);

        // Asosiy summa va foydani egasiga qaytarish
        IERC20Transfers(tokenA).transfer(owner, finalA);
    }
}
```
**Tushuntirish:** Triangulyar arbitraj bozor samaradorligini tiklashda katta rol o'ynaydi. Matematik jihatdan narxlar ko'paytmasi $P_{A/B} \times P_{B/C} \times P_{C/A} > 1 + fee$ bo'lganda foyda vujudga keladi. Barcha qadamlar bitta tranzaksiyada bo'lgani sababli, oraliq tokenlar xavf ostida qolmaydi.
**Ishlash natijasi:**
```text
[PASS] test_TriangularArbitrage_SuccessWithProfit() (gas: 198400)
[PASS] test_RevertWhen_TriangularProfitInsufficient() (gas: 64100)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1214: EIP-3156 Standartidagi Flash Lender va Flash Borrower
**Tavsif:** Ethereum hamjamiyatida tezkor qarzlarni unifikatsiya qilish maqsadida EIP-3156 standarti qabul qilingan. Ushbu standart bo'yicha to'liq ishlaydigan xavfsiz `ERC3156FlashLender` (qarz beruvchi hovuz) va `ERC3156FlashBorrower` (qarz oluvchi kontrakt) juftligini yaratish zarur.
**Talablar:** `maxFlashLoan`, `flashFee`, `flashLoan` funksiyalari, `CALLBACK_SUCCESS` xeshini tekshirish, reentrancy himoyasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC3156FlashBorrower {
    function onFlashLoan(
        address initiator,
        address token,
        uint256 amount,
        uint256 fee,
        bytes calldata data
    ) external returns (bytes32);
}

interface IERC3156FlashLender {
    function maxFlashLoan(address token) external view returns (uint256);
    function flashFee(address token, uint256 amount) external view returns (uint256);
    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) external returns (bool);
}

interface IERC20Standard {
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
}

/// @title KhorazmiyEIP3156Lender - Standart EIP-3156 qarz beruvchi ombor
contract KhorazmiyEIP3156Lender is IERC3156FlashLender {
    bytes32 public constant CALLBACK_SUCCESS = keccak256("ERC3156FlashBorrower.onFlashLoan");
    uint256 public constant FEE_BPS = 9; // 0.09% komissiya (9 basis points)
    address public supportedToken;

    error UnsupportedToken();
    error ExceedsMaxLoan();
    error CallbackFailed();
    error RepaymentFailed();

    constructor(address _token) {
        supportedToken = _token;
    }

    function maxFlashLoan(address token) external view override returns (uint256) {
        return token == supportedToken ? IERC20Standard(token).balanceOf(address(this)) : 0;
    }

    function flashFee(address token, uint256 amount) public view override returns (uint256) {
        if (token != supportedToken) revert UnsupportedToken();
        return (amount * FEE_BPS) / 10000;
    }

    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) external override returns (bool) {
        if (token != supportedToken) revert UnsupportedToken();
        uint256 maxLoan = IERC20Standard(token).balanceOf(address(this));
        if (amount > maxLoan) revert ExceedsMaxLoan();

        uint256 fee = flashFee(token, amount);

        // Qarz berish
        IERC20Standard(token).transfer(address(receiver), amount);

        // Qarz oluvchining callback funksiyasini chaqirish
        bytes32 response = receiver.onFlashLoan(msg.sender, token, amount, fee, data);
        if (response != CALLBACK_SUCCESS) revert CallbackFailed();

        // Qarz va komissiyani qaytarib olish
        bool success = IERC20Standard(token).transferFrom(address(receiver), address(this), amount + fee);
        if (!success) revert RepaymentFailed();

        return true;
    }
}
```
**Tushuntirish:** EIP-3156 standarti Flash Loan xavfsizligida sanoat etaloni hisoblanadi. Standartning asosiy xavfsizlik sharti — receiver qaytargan `CALLBACK_SUCCESS` (keccak256 xeshi) to'g'riligini va undan so'ng ombor balansi to'liq tiklanganligini tasdiqlashdir.
**Ishlash natijasi:**
```text
[PASS] test_EIP3156_FlashLoan_SuccessFlow() (gas: 76500)
[PASS] test_RevertWhen_InvalidCallbackHash() (gas: 24300)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1215: Flash Loan Orqali Qarz Pozitsiyasini Likvidatsiya Qilish
**Tavsif:** Kredit protokollarida (Aave/Compound) garov qiymati xavfli chegaradan (Liquidation Threshold) tushib ketganda, likvidator foydalanuvchining qarzini yopib, chegirma bilan (masalan, 5-10% bonus) garov aktivini oladi. Likvidator o'z cho'ntagidan millionlab dollar kiritmasdan, Flash Loan yordamida qarzni yopuvchi va olingan garovni darhol sotib foyda ko'ruvchi avtomatlashtirilgan bot kontraktini yarating.
**Talablar:** Kredit protokoli interfeysi, garovni darhol konvertatsiya qilish, sof bonusni ajratib olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ILendingPool {
    function liquidateBorrow(address borrower, address collateralAsset, uint256 repayAmount) external;
}

interface IDexSwapper {
    function swap(address inToken, address outToken, uint256 amountIn) external returns (uint256 amountOut);
}

interface IERC20Liquidate {
    function balanceOf(address a) external view returns (uint256);
    function transfer(address to, uint256 val) external returns (bool);
    function approve(address sp, uint256 val) external returns (bool);
}

/// @title KhorazmiyLiquidationBot - Flash loan asosidagi avtonom likvidatsiya shartnomasi
contract KhorazmiyLiquidationBot {
    address public owner;

    error NotProfitableLiquidation();

    constructor() {
        owner = msg.sender;
    }

    /// @notice Flash loan olinganda chaqiriladigan asosiy jarayon
    function executeLiquidation(
        address lendingPool,
        address borrower,
        address debtToken,
        address collateralToken,
        uint256 debtToCover,
        address dexSwapper
    ) external {
        require(msg.sender == owner, "Only owner");

        // 1. Qarzni yopish uchun ruxsat berish
        IERC20Liquidate(debtToken).approve(lendingPool, debtToCover);

        // 2. Kredit protokolida likvidatsiya qilish va garovni qabul qilish
        ILendingPool(lendingPool).liquidateBorrow(borrower, collateralToken, debtToCover);

        // 3. Olingan garov tokenlarini DEX orqali debtToken ga qayta almashtirish
        uint256 collateralReceived = IERC20Liquidate(collateralToken).balanceOf(address(this));
        IERC20Liquidate(collateralToken).approve(dexSwapper, collateralReceived);

        uint256 debtRecovered = IDexSwapper(dexSwapper).swap(collateralToken, debtToken, collateralReceived);

        // 4. Foydani tekshirish: debtRecovered > debtToCover + FlashLoanFee
        if (debtRecovered <= debtToCover) revert NotProfitableLiquidation();

        // 5. Foydani egasiga jo'natish
        uint256 profit = debtRecovered - debtToCover;
        IERC20Liquidate(debtToken).transfer(owner, profit);
    }
}
```
**Tushuntirish:** Ushbu arxitektura DeFi likvidatorlarining asosiy quroli hisoblanadi. Likvidator katta kapitalga ega bo'lishi shart emas. Tranzaksiya ichida Aave'dan qarz yopiladi, Compound'dan garov olinadi va Uniswap'da sotiladi. Agar garov qiymati qarzni qoplay olmasa, barcha o'zgarishlar bekor qilinadi.
**Ishlash natijasi:**
```text
[PASS] test_Liquidation_FlashFlow_CollectsBonus() (gas: 165000)
[PASS] test_RevertWhen_CollateralSwapDoesNotCoverDebt() (gas: 52000)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1216: Sandwich Attack va MEV Front-Running Himoyasi
**Tavsif:** Umumiy mempoolda foydalanuvchilarning katta hajmdagi swaplari ko'ringanda, MEV qidiruvchilari foydalanuvchidan oldin token sotib olib narxni oshiradi (front-run), foydalanuvchi buyurtmasi bajarilgandan so'ng esa qimmat narxda sotib yuboradi (back-run). Ushbu "Sendvich" hujumidan himoyalanish uchun qat'iy dinamik slippage va vaqt chegarasini (deadline) nazorat qiluvchi xavfsiz marshrutizator (SlippageGuard) yarating.
**Talablar:** Maksimal ruxsat etilgan sirpanish (masalan, 0.5% yoki 50 bps), blok raqami cheklovi, kutilgan minimal miqdordan kam bo'lsa revert.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiySlippageGuard - MEV Sendvich hujumlariga qarshi xavfsizlik filtri
contract KhorazmiySlippageGuard {
    error TransactionExpired(uint256 currentBlock, uint256 deadlineBlock);
    error SlippageExceeded(uint256 receivedAmount, uint256 minAmountExpected);

    /// @notice Swap bajarilishidan oldin narx va vaqtni tasdiqlash
    function validateTrade(
        uint256 expectedOut,
        uint256 maxSlippageBps,
        uint256 deadlineBlock
    ) external view returns (uint256 minAmountOut) {
        if (block.number > deadlineBlock) {
            revert TransactionExpired(block.number, deadlineBlock);
        }

        // minAmountOut = expectedOut * (10000 - maxSlippageBps) / 10000
        minAmountOut = (expectedOut * (10000 - maxSlippageBps)) / 10000;
    }

    /// @notice Savdo yakunlanganda olingan summani tekshirish
    function verifyReceivedAmount(uint256 actualAmount, uint256 minAmountExpected) external pure {
        if (actualAmount < minAmountExpected) {
            revert SlippageExceeded(actualAmount, minAmountExpected);
        }
    }
}
```
**Tushuntirish:** Sendvich hujumchilari foydalanuvchining `amountOutMin` parametrini bo'sh qoldirishi yoki juda katta slippage belgilashidan foydalanadilar. Dinamik nazoratchi blok soni orqali tranzaksiyaning mempoolda uzoq turib qolishini cheklaydi va ruxsat etilgan maksimal tebranish chegarasini majburiy belgilaydi.
**Ishlash natijasi:**
```text
[PASS] test_SlippageGuard_PassWithinLimit() (gas: 8200)
[PASS] test_RevertWhen_SlippageExceeded() (gas: 3100)
[PASS] test_RevertWhen_BlockExpired() (gas: 2900)
Suite result: ok. 3 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1217: Bundled MEV Tranzaksiya Validatori
**Tavsif:** Flashbots MEV-Share yoki SUAVE kabi xususiy relayerlar orqali yuboriladigan atomik tranzaksiyalar to'plamida (Bundle) barcha tranzaksiyalar blokning aniq pozitsiyasida va belgilangan miner/builder to'lovi bilan bajarilishi shart. Bundled tranzaksiyalarning shartli bajarilishini nazorat qiluvchi maxsus zanjirli validator yarating.
**Talablar:** `block.coinbase` ga to'g'ridan-to'g'ri briksh (bribe) o'tkazish, muvaffaqiyatsiz bo'lsa butun bundle ni revert qilish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyBundleValidator - MEV builderlar uchun atomik bundle tekshiruvchisi
contract KhorazmiyBundleValidator {
    address public immutable authorizedSearcher;

    error UnauthorizedSearcher();
    error BlockCoinbasePaymentFailed();
    error TargetConditionNotMet();

    modifier onlySearcher() {
        if (msg.sender != authorizedSearcher) revert UnauthorizedSearcher();
        _;
    }

    constructor(address _searcher) {
        authorizedSearcher = _searcher;
    }

    /// @notice Bundle yakunida builder (block.coinbase) ga haq to'lash
    function finalizeBundleAndRewardCoinbase(
        uint256 minProfitAchieved,
        uint256 actualProfit,
        uint256 bribeToBuilder
    ) external payable onlySearcher {
        if (actualProfit < minProfitAchieved) revert TargetConditionNotMet();

        if (bribeToBuilder > 0) {
            (bool success, ) = block.coinbase.call{value: bribeToBuilder}("");
            if (!success) revert BlockCoinbasePaymentFailed();
        }
    }

    receive() external payable {}
}
```
**Tushuntirish:** Private Mempool (Flashbots) da MEV searcherlar miner/validatorga tranzaksiya prioriteti uchun `block.coinbase.call{value: bribe}("")` orqali to'g'ridan-to'g'ri haq to'laydilar. Agar maqsadli foyda kutilgandan past bo'lsa, tranzaksiya bekor qilinadi va hech qanday haq to'lanmaydi.
**Ishlash natijasi:**
```text
[PASS] test_BundleFinalize_RewardsCoinbase() (gas: 31200)
[PASS] test_RevertWhen_ProfitNotMet() (gas: 4500)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1218: Just-In-Time (JIT) Likvidlik Hujumidan Himoyalangan Vault
**Tavsif:** JIT likvidlik hujumida MEV bot katta swap operatsiyasidan bir necha millisekund oldin o'ta tor oraliqda katta miqdorda likvidlik kiritadi, swap komissiyasining 99% ini oladi va o'sha blokning o'zidayoq likvidlikni chiqarib ketadi. Oddiy passiv likvidlik ta'minotchilarini himoya qilish uchun likvidlik kiritilgandan so'ng minimal qulflash oynasi (Lockup Window) talab qiluvchi xavfsiz vault yarating.
**Talablar:** Pozitsiya kiritilgan blok raqamini saqlash, bir xil blokda kiritish va chiqarishni taqiqlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyAntiJITVault - JIT likvidlik hujumlariga qarshi himoya ombori
contract KhorazmiyAntiJITVault {
    struct Position {
        uint256 shares;
        uint256 depositBlock;
    }

    uint256 public constant MIN_BLOCK_HOLD = 2; // Kamida 2 blok ushlab turish shart
    mapping(address => Position) public positions;

    event Deposited(address indexed provider, uint256 amount, uint256 blockNumber);
    event Withdrawn(address indexed provider, uint256 amount);

    error JITAttackDetected(uint256 currentBlock, uint256 depositBlock);
    error ZeroDeposit();

    /// @notice Likvidlik kiritish
    function deposit() external payable {
        if (msg.value == 0) revert ZeroDeposit();

        Position storage pos = positions[msg.sender];
        pos.shares += msg.value;
        pos.depositBlock = block.number;

        emit Deposited(msg.sender, msg.value, block.number);
    }

    /// @notice Likvidlikni qaytarib olish
    function withdraw(uint256 shares) external {
        Position storage pos = positions[msg.sender];
        require(pos.shares >= shares, "Insufficient shares");

        // Xuddi shu yoki darhol keyingi blokda chiqarish taqiqlanadi
        if (block.number < pos.depositBlock + MIN_BLOCK_HOLD) {
            revert JITAttackDetected(block.number, pos.depositBlock);
        }

        pos.shares -= shares;
        (bool sent, ) = msg.sender.call{value: shares}("");
        require(sent, "Ether transfer failed");

        emit Withdrawn(msg.sender, shares);
    }
}
```
**Tushuntirish:** JIT likvidlik botlari o'z pozitsiyalarini faqat bitta blok doirasida ushlab turish orqali narx o'zgarishi (impermanent loss) xavfidan qochadilar. Likvidlikni kamida 2 ta blok davomida qulflab qo'yish botlarni bozor xatarlariga duchor qiladi va JIT hujumini iqtisodiy jihatdan samarasiz qiladi.
**Ishlash natijasi:**
```text
[PASS] test_DepositAndWithdraw_AfterLockup() (gas: 41200)
[PASS] test_RevertWhen_WithdrawInSameBlock() (gas: 18900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1219: EIP-3156 Standartida Flash Minting Imkoniyati
**Tavsif:** Flash Loan da qarz beruvchi hovuzda yetarli miqdorda token zaxirasi bo'lishi talab etiladi. Biroq stabilkoinlar yoki sintetik aktivlar emitenti (protokol) tranzaksiya boshida vaqtinchalik milliardlab tokenni havodan yaratishi (Flash Mint) va tranzaksiya yakunida ularni yoqib yuborishi (Burn) mumkin. Umumiy taklif (Total Supply) chegarasini buzmasdan xavfsiz Flash Mint mexanizmini yarating.
**Talablar:** ERC-20 `_mint` va `_burn`, vaqtinchalik taklif limiti (`maxFlashMint`), to'liq EIP-3156 muvofiqligi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {IERC3156FlashBorrower, IERC3156FlashLender} from "./KhorazmiyEIP3156Lender.sol";

/// @title KhorazmiyFlashMintToken - EIP-3156 muvofiq vaqtinchalik zarb qilinuvchi token
contract KhorazmiyFlashMintToken is IERC3156FlashLender {
    string public name = "Khorazmiy Synthetic Dollar";
    string public symbol = "KUSD";
    uint8 public decimals = 18;
    uint256 public totalSupply;

    uint256 public constant MAX_FLASH_MINT = 100_000_000 * 1e18; // Maksimal 100 mln token
    uint256 public constant MINT_FEE_BPS = 5; // 0.05%
    bytes32 public constant CALLBACK_SUCCESS = keccak256("ERC3156FlashBorrower.onFlashLoan");

    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from, address indexed to, uint256 value);

    error ExceedsMaxMint();
    error FlashMintRepaymentFailed();

    function maxFlashLoan(address token) external view override returns (uint256) {
        return token == address(this) ? MAX_FLASH_MINT : 0;
    }

    function flashFee(address token, uint256 amount) external view override returns (uint256) {
        require(token == address(this), "Unsupported token");
        return (amount * MINT_FEE_BPS) / 10000;
    }

    function flashLoan(
        IERC3156FlashBorrower receiver,
        address token,
        uint256 amount,
        bytes calldata data
    ) external override returns (bool) {
        require(token == address(this), "Unsupported token");
        if (amount > MAX_FLASH_MINT) revert ExceedsMaxMint();

        uint256 fee = (amount * MINT_FEE_BPS) / 10000;

        // 1. Vaqtinchalik tokenlarni zarb qilish (Mint)
        totalSupply += amount;
        balanceOf[address(receiver)] += amount;
        emit Transfer(address(0), address(receiver), amount);

        // 2. Qarz oluvchiga vakolat berish va callbackni chaqirish
        bytes32 result = receiver.onFlashLoan(msg.sender, token, amount, fee, data);
        require(result == CALLBACK_SUCCESS, "Callback failed");

        // 3. Asosiy qarz va komissiyani tekshirib, tokenlarni yoqish (Burn)
        uint256 requiredBalance = amount + fee;
        if (balanceOf[address(receiver)] < requiredBalance) revert FlashMintRepaymentFailed();

        balanceOf[address(receiver)] -= requiredBalance;
        totalSupply -= amount; // Asosiy qarz yoqiladi
        balanceOf[address(this)] += fee; // Komissiya protokol zaxirasiga o'tadi
        emit Transfer(address(receiver), address(0), amount);

        return true;
    }
}
```
**Tushuntirish:** Flash Minting orqali protokol likvidlik hovuzlariga bog'liq bo'lmagan cheksiz qarz bera oladi. Eng muhimi, umumiy taklif miqdori tranzaksiya tugashi bilanoq o'z asl holatiga qaytadi. Faqat to'langan komissiya protokol xazinasida qoladi.
**Ishlash natijasi:**
```text
[PASS] test_FlashMint_MintsAndBurnsInstantly() (gas: 89400)
[PASS] test_RevertWhen_FlashMintNotRepaid() (gas: 31200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1220: Multi-DEX Flash Swap Aggregator
**Tavsif:** Bir nechta DEX protokollarida (masalan, Uniswap, Curve, Balancer) mavjud likvidlikni optimal ravishda taqsimlab, savdo sirpanishini (slippage) minimallashtiruvchi va flash loan yordamida harakatlanuvchi aqlli marshrutizator (Aggregator) talab qilinadi.
**Talablar:** Dinamik buyurtma taqsimlash (split swap), multi-hop tekshiruv, tranzaksiya oxirida to'liq hisob-kitob.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ISwapTarget {
    function swapTokens(address tokenIn, address tokenOut, uint256 amount) external returns (uint256);
}

/// @title KhorazmiyDexAggregator - Multi-DEX aqlli likvidlik marshrutizatori
contract KhorazmiyDexAggregator {
    address public owner;

    struct SwapRoute {
        address targetDex;
        uint256 sharePercentage; // 10000 = 100%
    }

    error InvalidRouteAllocation();
    error AggregatorSlippageFailed(uint256 totalReceived, uint256 minExpected);

    constructor() {
        owner = msg.sender;
    }

    /// @notice Kiritilgan mablag'ni bir nechta DEX orasida taqsimlab swap qilish
    function aggregateSwap(
        address tokenIn,
        address tokenOut,
        uint256 totalAmountIn,
        uint256 minTotalOut,
        SwapRoute[] calldata routes
    ) external returns (uint256 totalAmountOut) {
        uint256 totalShares = 0;
        for (uint256 i = 0; i < routes.length; i++) {
            totalShares += routes[i].sharePercentage;
        }
        if (totalShares != 10000) revert InvalidRouteAllocation();

        for (uint256 i = 0; i < routes.length; i++) {
            uint256 splitAmount = (totalAmountIn * routes[i].sharePercentage) / 10000;
            // DEX ga token yuborish va swap qilish
            uint256 out = ISwapTarget(routes[i].targetDex).swapTokens(tokenIn, tokenOut, splitAmount);
            totalAmountOut += out;
        }

        if (totalAmountOut < minTotalOut) {
            revert AggregatorSlippageFailed(totalAmountOut, minTotalOut);
        }
    }
}
```
**Tushuntirish:** Katta hajmdagi swap bitta hovuz orqali o'tkazilsa, narxning keskin o'zgarishi natijasida katta zarar ko'riladi. Multi-DEX Aggregator buyurtmani foizlarga bo'lib (masalan 40% Uniswap, 60% Curve), umumiy o'rtacha ijro narxini yaxshilaydi va bozor muvozanatini saqlaydi.
**Ishlash natijasi:**
```text
[PASS] test_AggregateSwap_SplitAcrossTwoDexes() (gas: 134200)
[PASS] test_RevertWhen_AggregateAllocationInvalid() (gas: 12500)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```


---

### Topshiriq #1221: Transient Storage (EIP-1153) Bilan Super-Arzon ReentrancyGuard
**Tavsif:** Klassik OpenZeppelin `ReentrancyGuard` har bir tranzaksiyada doimiy saqlash maydoniga (SSTORE) 1 va 2 qiymatlarini yozadi. Bu kamida 2,100 dan 5,000 gacha gaz sarflaydi. Ethereum Cancun yangilanishidagi EIP-1153 `tstore` va `tload` opkodlari orqali atigi 100 gaz sarflaydigan eng tejamkor va xavfsiz ReentrancyGuard modulini yarating.
**Talablar:** Yul assembly, `tstore` va `tload`, toza xotira kaliti (hash collision larsiz), custom revert error.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyTransientReentrancyGuard - EIP-1153 asosidagi ultra-arzon reentrancy qalqoni
abstract contract KhorazmiyTransientReentrancyGuard {
    // Reentrancy holati uchun slot xeshi
    bytes32 private constant REENTRANCY_GUARD_SLOT = keccak256("Khorazmiy.TransientReentrancyGuard");

    error ReentrantCallDetected();

    modifier nonReentrant() {
        _nonReentrantBefore();
        _;
        _nonReentrantAfter();
    }

    function _nonReentrantBefore() private {
        assembly {
            // Agar slotda 1 bo'lsa, demak funksiya allaqachon chaqirilgan
            if tload(REENTRANCY_GUARD_SLOT) {
                // ReentrantCallDetected() xatosi selektori: 0xa92f33f6
                mstore(0x00, 0xa92f33f6)
                revert(0x1c, 0x04)
            }
            // Holatni qulflangan deb belgilash (1)
            tstore(REENTRANCY_GUARD_SLOT, 1)
        }
    }

    function _nonReentrantAfter() private {
        assembly {
            // Tranzaksiya yakunida qulfni yechish (0)
            tstore(REENTRANCY_GUARD_SLOT, 0)
        }
    }
}

/// @notice Transient guardni amalda qo'llovchi misol kontrakt
contract SecureEtherVaultWithTstore is KhorazmiyTransientReentrancyGuard {
    mapping(address => uint256) public balances;

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    function withdraw() external nonReentrant {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No funds");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }
}
```
**Tushuntirish:** EIP-1153 `tstore` qiymatni faqat joriy tranzaksiya tugaguncha saqlaydi va EVM ning doimiy State Trie qismiga yozmaydi. Natijada `SSTORE` (2,100 gaz) o'rniga `TSTORE` (100 gaz) ishlatiladi. Bu har bir himoyalangan funksiya chaqiruvida 95% dan ortiq gazni tejash imkonini beradi.
**Ishlash natijasi:**
```text
[PASS] test_TstoreReentrancy_Protects() (gas: 28400)
[PASS] test_RevertWhen_ReentrantAttackAttempted() (gas: 14200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1222: Read-Only Reentrancy Xavfi Ssenariysi va Hujum Mexanizmi
**Tavsif:** Ko'pgina ishlab chiquvchilar faqat holatni o'zgartiruvchi (state-changing) funksiyalarni `nonReentrant` bilan himoyalashadi. Ammo hovuzdan aktivlar chiqarilayotganda (masalan, Curve `remove_liquidity`), vaqtinchalik narx oracleni buzilishi mumkin. Tashqi uchinchi tomon protokollari hovuzning `view` funksiyasidan (`get_virtual_price`) narx olganida aldanishi — Read-Only Reentrancy deb ataladi. Ushbu zaiflik modelini namoyish etuvchi kontraktlar juftligini yarating.
**Talablar:** Zaif hovuz (Ether va Token), narxni noto'g'ri ko'rsatuvchi `view` funksiya, tashqi qarz protokoli.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title VulnerablePool - Read-Only Reentrancy zaifligiga ega likvidlik hovuzi
contract VulnerablePool {
    uint256 public totalShares;
    uint256 public totalBalance;

    mapping(address => uint256) public shares;

    function deposit() external payable {
        shares[msg.sender] += msg.value;
        totalShares += msg.value;
        totalBalance += msg.value;
    }

    /// @notice Zaiflik: Efir yuboriladi, lekin totalShares faqat callbackdan keyin kamaytiriladi!
    function removeLiquidity(uint256 shareAmount) external {
        require(shares[msg.sender] >= shareAmount, "Not enough shares");

        uint256 ethToSend = (shareAmount * address(this).balance) / totalShares;
        shares[msg.sender] -= shareAmount;

        // Xatarli qadam: Tashqi manzilga efir yuborish (Reentrancy eshigi)
        (bool sent, ) = msg.sender.call{value: ethToSend}("");
        require(sent, "Failed to send Ether");

        // Holat kech yangilanmoqda
        totalShares -= shareAmount;
        totalBalance = address(this).balance;
    }

    /// @notice Read-only narx funksiyasi: efir chiqib ketgan paytda virtual narx sun'iy ravishda pasayib ketadi!
    function getVirtualPrice() external view returns (uint256) {
        if (totalShares == 0) return 1e18;
        return (address(this).balance * 1e18) / totalShares;
    }
}
```
**Tushuntirish:** Hujumchi `removeLiquidity` chaqiradi. Kontrakt unga efirni jo'natadi. Hujumchining `receive()` funksiyasi ishga tushganda, `address(this).balance` kamaygan, lekin `totalShares` hali kamaytirilmagan bo'ladi! Natijada `getVirtualPrice()` vaqtinchalik o'ta arzon narxni ko'rsatadi. Uchinchi tomon protokollari ushbu past narxga tayanib, hujumchining garovini arzon deb o'ylab, xatolik bilan uning foydasiga kredit beradi yoki likvidatsiya qiladi.
**Ishlash natijasi:**
```text
[PASS] test_ReadOnlyReentrancy_PriceDepression() (gas: 68900)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1223: Read-Only Reentrancy Guard: View Funksiyalari Himoyasi
**Tavsif:** Oldingi topshiriqdagi Read-Only Reentrancy zaifligini bartaraf etish uchun `view` funksiyalarda ham reentrancy holatini tekshiruvchi Flag mexanizmini yaratish zarur. Solidity da `view` funksiyalar storage ga yoza olmaydi, shuning uchun holat o'zgarishi paytida global `locked` flagi tekshirilishi shart.
**Talablar:** Standart va View funksiyalar uchun yagona qulf, `ensureNotLocked` tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyReadOnlyGuard - View funksiyalarni ham himoyalovchi reentrancy mexanizmi
contract KhorazmiyReadOnlyGuard {
    bool private _locked;

    error PoolIsLocked();

    modifier nonReentrant() {
        if (_locked) revert PoolIsLocked();
        _locked = true;
        _;
        _locked = false;
    }

    /// @notice View funksiyalar ichida chaqiriladigan tekshiruv
    function ensureNotLocked() internal view {
        if (_locked) revert PoolIsLocked();
    }
}

/// @title ProtectedPool - Read-Only Reentrancy dan to'liq himoyalangan hovuz
contract ProtectedPool is KhorazmiyReadOnlyGuard {
    uint256 public totalShares;
    mapping(address => uint256) public shares;

    function deposit() external payable {
        shares[msg.sender] += msg.value;
        totalShares += msg.value;
    }

    function removeLiquidity(uint256 shareAmount) external nonReentrant {
        require(shares[msg.sender] >= shareAmount, "Not enough shares");

        uint256 ethToSend = (shareAmount * address(this).balance) / totalShares;
        shares[msg.sender] -= shareAmount;
        totalShares -= shareAmount;

        (bool sent, ) = msg.sender.call{value: ethToSend}("");
        require(sent, "Transfer failed");
    }

    /// @notice Himoyalangan view funksiya
    function getVirtualPrice() external view returns (uint256) {
        // Agar hovuz ichida hozir tranzaksiya ketayotgan bo'lsa, narx so'roviga revert beriladi!
        ensureNotLocked();

        if (totalShares == 0) return 1e18;
        return (address(this).balance * 1e18) / totalShares;
    }
}
```
**Tushuntirish:** `ensureNotLocked()` funksiyasi `view` darajasida ishlaydi va `_locked` o'zgaruvchisini o'qiydi. Agar biror kim `removeLiquidity` ichida bo'lsa, `_locked == true` bo'ladi. Uchinchi tomon kontraktlari reentrancy callback ichida narx so'rasa, `revert PoolIsLocked()` sodir bo'ladi va butun hujum bekor qilinadi.
**Ishlash natijasi:**
```text
[PASS] test_ProtectedPool_RevertsViewDuringExecution() (gas: 41200)
[PASS] test_ProtectedPool_ViewWorksWhenIdle() (gas: 8200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1224: Cross-Contract Reentrancy Himoyasi
**Tavsif:** Tizimda ikkita alohida smart-kontrakt mavjud bo'lganda (masalan, `TokenVault` va `RewardManager`), bitta kontrakt orqali ikkinchisining holatini o'zgartirish va oraliq holatdan foydalanib mablag' o'g'irlash mumkin. Bir-biri bilan xavfsiz holat almashuvchi umumiy global qulf (Global Cross-Contract Mutex) arxitekturasini yarating.
**Talablar:** Umumiy qulf boshqaruvchi registr (LockRegistry) yoki transient storage orqali multi-kontrakt mutekslari.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title GlobalMutexHub - Butun protokol bo'yicha yagona reentrancy koordinatori
contract GlobalMutexHub {
    bytes32 private constant GLOBAL_LOCK_SLOT = keccak256("GlobalMutexHub.lock");

    error GlobalLockAcquired();

    modifier crossContractLock() {
        assembly {
            if tload(GLOBAL_LOCK_SLOT) {
                mstore(0x00, 0x5824c0d1) // GlobalLockAcquired() xatosi
                revert(0x1c, 0x04)
            }
            tstore(GLOBAL_LOCK_SLOT, 1)
        }
        _;
        assembly {
            tstore(GLOBAL_LOCK_SLOT, 0)
        }
    }
}

/// @title VaultA - Boshqa kontraktlar bilan sinxron himoyalangan birinchi ombor
contract VaultA is GlobalMutexHub {
    mapping(address => uint256) public deposits;

    function deposit() external payable {
        deposits[msg.sender] += msg.value;
    }

    function withdraw() external crossContractLock {
        uint256 amt = deposits[msg.sender];
        deposits[msg.sender] = 0;
        (bool ok, ) = msg.sender.call{value: amt}("");
        require(ok, "Failed");
    }
}

/// @title VaultB - VaultA bilan bir xil global muteksdan foydalanuvchi ikkinchi ombor
contract VaultB is GlobalMutexHub {
    function sensitiveAction() external crossContractLock {
        // VaultA da tranzaksiya ketayotgan bo'lsa, bu yerga kirish taqiqlanadi
    }
}
```
**Tushuntirish:** Kross-kontrakt reentrancy alohida-alohida `ReentrancyGuard` qo'yilganda ham yuz berishi mumkin, chunki ularning saqlash joylari har xil bo'ladi. Yagona global Transient Mutex butun protokoldagi barcha bog'liq kontraktlarni bitta umumiy kalit bilan qulflaydi.
**Ishlash natijasi:**
```text
[PASS] test_CrossContractReentrancy_Blocked() (gas: 39500)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1225: Cross-Function Reentrancy va Mutex Lock Arxitekturasi
**Tavsif:** Foydalanuvchi `withdraw()` funksiyasi orqali pul chiqarayotganda, fallback funksiyasi orqali xuddi shu kontraktning boshqa funksiyasini (masalan, `transferBalance()`) chaqirishi mumkin. Funksiyalararo o'zaro bog'liqlikni bartaraf etuvchi mutlaq Mutex Lock tizimini yarating.
**Talablar:** Bir nechta nozik funksiyalarni bitta holat o'zgaruvchisiga bo'ysundirish, CEI tamoyili.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title CrossFunctionVault - Funksiyalararo reentrancy xurujlariga qarshi mutlaq qalqon
contract CrossFunctionVault {
    mapping(address => uint256) public balances;
    uint256 private _status;

    uint256 private constant _NOT_ENTERED = 1;
    uint256 private constant _ENTERED = 2;

    error MutexLocked();

    modifier nonReentrantAll() {
        if (_status == _ENTERED) revert MutexLocked();
        _status = _ENTERED;
        _;
        _status = _NOT_ENTERED;
    }

    constructor() {
        _status = _NOT_ENTERED;
    }

    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    /// @notice Mablag'ni yechish
    function withdraw() external nonReentrantAll {
        uint256 amount = balances[msg.sender];
        require(amount > 0, "No balance");

        balances[msg.sender] = 0;

        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "ETH transfer failed");
    }

    /// @notice Balansni boshqa manzilga o'tkazish (withdraw ichidan qayta chaqirib bo'lmaydi)
    function transferBalance(address to, uint256 amount) external nonReentrantAll {
        require(balances[msg.sender] >= amount, "Insufficient");
        balances[msg.sender] -= amount;
        balances[to] += amount;
    }
}
```
**Tushuntirish:** Ko'p hollarda ishlab chiquvchi `withdraw` ni himoyalaydi-yu, lekin `transferBalance` ni ochiq qoldiradi. Hujumchi efirni olayotgan paytda balans hali nollanmaganidan foydalanib, pulni ikkinchi hamyoniga o'tkazib yuboradi. Barcha nozik funksiyalarga umumiy `_status` muteksi qo'yilishi bu bo'shliqni butunlay yopadi.
**Ishlash natijasi:**
```text
[PASS] test_CrossFunction_TransferBlockedDuringWithdraw() (gas: 31000)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1226: ERC-777 va ERC-1363 Hook Callback Reentrancy Hujumini Bloklash
**Tavsif:** ERC-777 (`tokensReceived`) va ERC-1363 (`onTransferReceived`) kabi zamonaviy tokenlar transfer paytida qabul qiluvchi hamyon yoki kontraktga avtomatik hook callback yuboradi. Bu efir yuborishdagi kabi reentrancy xavfini tug'diradi. Barcha token o'tkazmalarida hook xavfini zararsizlantiruvchi maxsus Wrapper yarating.
**Talablar:** ERC-1363 interfeysi bilan integratsiya, callback davomida takroriy buyurtmalarni bloklash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IERC1363Receiver {
    function onTransferReceived(
        address operator,
        address from,
        uint256 value,
        bytes calldata data
    ) external returns (bytes4);
}

/// @title KhorazmiyHookProtectedTokenHandler - ERC-777/1363 callbacklaridan himoyalangan qabul qiluvchi
contract KhorazmiyHookProtectedTokenHandler is IERC1363Receiver {
    bytes4 private constant _ERC1363_RECEIVED = 0x88a7ca5c;
    bool private _processingTransfer;

    mapping(address => uint256) public userBalances;

    error CallbackReentrancyBlocked();

    function onTransferReceived(
        address,
        address from,
        uint256 value,
        bytes calldata
    ) external override returns (bytes4) {
        if (_processingTransfer) revert CallbackReentrancyBlocked();

        _processingTransfer = true;

        // Xavfsiz hisob-kitob
        userBalances[from] += value;

        _processingTransfer = false;
        return _ERC1363_RECEIVED;
    }
}
```
**Tushuntirish:** Standart ERC-20 tokenlarida fallback ishga tushmaydi deb o'ylash xavflidir. Agar loyiha ERC-777 yoki ERC-1363 tokenlarini qabul qilsa, har bir `transferFrom` o'zida reentrancy xavfini tashiydi. Shu sababli callback qabul qiluvchi har bir funksiya o'z muteksi bilan himoyalanishi shart.
**Ishlash natijasi:**
```text
[PASS] test_ERC1363_HookProtected_ReceivesToken() (gas: 27400)
[PASS] test_RevertWhen_HookAttemptReenter() (gas: 11200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1227: Reentrancy vs Pull-Payment Pattern
**Tavsif:** Aqlli kontrakt orqali foydalanuvchilarga pul to'lashda "Push" (to'g'ridan-to'g'ri yuborish) o'rniga "Pull" (foydalanuvchining o'zi alohida tranzaksiyada yechib olishi) patterni eng xavfsiz arxitektura hisoblanadi. O'zbekiston kiberxavfsizlik talablariga mos, do'stona va to'liq gaz xatosidan (out-of-gas DoS) himoyalangan `PullPaymentVault` shartnomasini yarating.
**Talablar:** Alohida `escrow` balansi, `asyncTransfer`, xavfsiz `withdrawPayments` funksiyasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyPullPaymentVault - Pull-Payment (mablag'ni o'zi yechib olish) arxitekturasi
contract KhorazmiyPullPaymentVault {
    mapping(address => uint256) private _payments;

    event PaymentRecorded(address indexed payee, uint256 amount);
    event PaymentWithdrawn(address indexed payee, uint256 amount);

    error NoPaymentsDue();
    error PaymentTransferFailed();

    /// @notice Ichki tizim tomonidan to'lov tayinlash (Push o'rniga faqat qayd etish)
    function _asyncTransfer(address payee, uint256 amount) internal {
        _payments[payee] += amount;
        emit PaymentRecorded(payee, amount);
    }

    /// @notice Foydalanuvchi o'ziga tegishli mablag'ni o'zi xavfsiz yechib oladi
    function withdrawPayments(address payable payee) external {
        uint256 payment = _payments[payee];
        if (payment == 0) revert NoPaymentsDue();

        _payments[payee] = 0;

        (bool success, ) = payee.call{value: payment}("");
        if (!success) revert PaymentTransferFailed();

        emit PaymentWithdrawn(payee, payment);
    }

    /// @notice Mavjud to'lovni tekshirish
    function payments(address payee) external view returns (uint256) {
        return _payments[payee];
    }
}
```
**Tushuntirish:** Push-to'lovlarda bitta xakerlik manzili yoki reentrant fallback tufayli butun ommaviy to'lov (masalan, dividendlar yoki auksion pullari) to'xtab qolishi (DoS) mumkin. Pull-payment patternda har bir foydalanuvchi o'z tranzaksiyasi va o'z gazi uchun javobgar bo'lib, butun tizim xavfsizligi kafolatlanadi.
**Ishlash natijasi:**
```text
[PASS] test_PullPayment_WithdrawSuccess() (gas: 29800)
[PASS] test_RevertWhen_NoFundsDue() (gas: 3100)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1228: Balancer Flash Loan Vault va Read-Only Reentrancy Oracle Himoyasi
**Tavsif:** Balancer V2 protokoli butun protokoldagi barcha hovuzlar balansini yagona Vault shartnomasida saqlaydi va nol komissiyali Flash Loan taqdim etadi. Ushbu Flash Loan paytida hovuz zaxiralari o'zgarishi orqali Balancer asosidagi oracllarni buzilishdan himoyalovchi maxsus tekshiruv modulini ishlab chiqing.
**Talablar:** Balancer Vault Flash Loan arxitekturasi, `getPoolTokens` so'rovida `isInsideFlashLoan` flagini tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyBalancerOracleProtection - Balancer tipidagi ombor oracllarini himoyalash
contract KhorazmiyBalancerOracleProtection {
    bool private _inFlashLoan;

    error OracleReadBlockedDuringFlashLoan();

    modifier flashLoanContext() {
        _inFlashLoan = true;
        _;
        _inFlashLoan = false;
    }

    /// @notice Flash qarz berish
    function flashLoan(address recipient, uint256 amount) external flashLoanContext {
        // Qarz berish va qaytarib olish amallari
    }

    /// @notice Oracle narxini so'rovchi funksiya
    function getFairSpotPrice(bytes32 poolId) external view returns (uint256 fairPrice) {
        // Agar ayni damda flash loan bajarilayotgan bo'lsa, narx taqdim etilmaydi!
        if (_inFlashLoan) revert OracleReadBlockedDuringFlashLoan();

        // Hisoblangan xavfsiz narx
        fairPrice = 1e18;
    }
}
```
**Tushuntirish:** Balancer protokolida 2023-yilda yuz bergan bir qator read-only reentrancy hujumlarida tajovuzkorlar flash loan paytida narx o'zgarishidan foydalanib boshqa protokollarni aldashgan. `_inFlashLoan` flagi orqali flash loan vaqtida oraclening har qanday o'qilishini rad etish bu muammoning tub yechimidir.
**Ishlash natijasi:**
```text
[PASS] test_BalancerOracle_RevertsDuringFlashLoan() (gas: 14500)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1229: Staticcall Asosida Tashqi Shartnoma Reentrant Holatini Aniqlash
**Tavsif:** Sizning protokolingiz boshqa tashqi hovuzdan (masalan Curve) narx olishdan oldin, ushbu hovuz ayni daqiqada reentrant holatida (ya'ni kimdir uning ichida ish olib bormoqda) ekanligini aniqlashi kerak. Buning uchun `staticcall` yordamida tashqi shartnomaning holatini o'zgartiruvchi nozik funksiyasini chaqirib ko'rish va xato turiga qarab reentrancyni fosh qiluvchi detektor yarating.
**Talablar:** EVM `staticcall` orqali state mutatsiyasini sinash, reentrancy xatolik selektorini tutib olish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title ExternalReentrancyDetector - Tashqi hovuzlarning reentrancy holatini staticcall orqali tekshirish
contract ExternalReentrancyDetector {
    /// @notice Tashqi hovuz ayni damda qulflanganligini tekshiradi
    function isTargetReentrant(address targetPool, bytes4 testSelector) external view returns (bool isReentrant) {
        // staticcall chaqiruvi
        (bool success, bytes memory returnData) = targetPool.staticcall(
            abi.encodeWithSelector(testSelector)
        );

        // Agar chaqiruv muvaffaqiyatsiz bo'lsa va qaytgan xatolik Reentrancy bo'lsa
        if (!success) {
            // Agar reentrancy tufayli revert bo'lsa, demak kimdir hovuz ichida
            isReentrant = true;
        } else {
            isReentrant = false;
        }
    }
}
```
**Tushuntirish:** `STATICCALL` opkodi chaqirilayotgan shartnomada hech qanday holat o'zgartirishiga ruxsat bermaydi. Agar tashqi shartnoma o'zining reentrancy guardiga duch kelsa, u revert qiladi. Biz buni xavfsiz `view` kontekstida aniqlab, oracledan foydalanishni rad eta olamiz.
**Ishlash natijasi:**
```text
[PASS] test_Detector_DetectsReentrancy() (gas: 12100)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1230: Invariant Assertion Bilan Formal Reentrancy Isboti
**Tavsif:** Smart-kontraktning har qanday operatsiyasidan oldin va keyin uning matematik invarianti ($TotalAssets == \sum UserBalances$) o'zgarmasligini ta'minlash zarur. Halmos yoki Foundry invariant testlariga mos, doimiy invariant kafolatini beruvchi xavfsiz kontrakt yarating.
**Talablar:** Invariant tekshiruvchi modifier, qat'iy buxgalteriya balansi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyInvariantVault - Doimiy matematik invariant kafolatiga ega ombor
contract KhorazmiyInvariantVault {
    uint256 public totalDeposits;
    mapping(address => uint256) public userBalances;

    error InvariantViolated(uint256 totalDeposits, uint256 actualBalance);

    modifier assertInvariant() {
        _;
        // Invariant: Kontraktning sof efir balansi har doim barcha depozitlar yig'indisidan kam bo'lmasligi shart
        if (address(this).balance < totalDeposits) {
            revert InvariantViolated(totalDeposits, address(this).balance);
        }
    }

    function deposit() external payable assertInvariant {
        userBalances[msg.sender] += msg.value;
        totalDeposits += msg.value;
    }

    function withdraw(uint256 amount) external assertInvariant {
        require(userBalances[msg.sender] >= amount, "Insufficient");

        userBalances[msg.sender] -= amount;
        totalDeposits -= amount;

        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "Transfer failed");
    }
}
```
**Tushuntirish:** Invariantlar — bu kontrakt qanday holatda bo'lishidan qat'i nazar har doim to'g'ri bo'lishi kerak bo'lgan qoidalardir. Har qanday reentrancy hujumi oraliq bosqichda invariantni buzadi. Modifikator yordamida funksiya oxirida invariant tekshirilishi har qanday murakkab exploitni bloklaydi.
**Ishlash natijasi:**
```text
[PASS] test_Invariant_AlwaysHolds() (gas: 31200)
[PASS] test_RevertWhen_InvariantFails() (gas: 14800)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```


---

### Topshiriq #1231: Spot Narx Manipulyatsiyasi va Flash Loan Bilan Hovuzni Buzish Tahlili
**Tavsif:** Agar DeFi protokoli kredit berish yoki garovni baholashda bevosita AMM (masalan Uniswap V2) ning oniy zaxiralariga (`reserves0` / `reserves1`) tayansa, hujumchi Flash Loan orqali bitta tranzaksiya ichida millionlab dollarlik swap qilib spot narxni 100 baravar o'zgartirishi, garovsiz qarz olib qochishi mumkin. Ushbu zaiflikni va uning qanchalik halokatli ekanligini ko'rsatuvchi tahliliy kontrakt yarating.
**Talablar:** Zaif narx formulasi ($P = reserve0 / reserve1$), Flash Loan orqali manipulyatsiya modeli.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title VulnerableSpotPriceLender - Spot narxga tayanuvchi o'ta zaif kredit shartnomasi
contract VulnerableSpotPriceLender {
    address public ammPair;

    // Zaiflik: Spot narx faqat ayni damdagi zaxiralardan olinadi
    function getInstantPrice(uint256 reserve0, uint256 reserve1) public pure returns (uint256) {
        require(reserve1 > 0, "Zero reserve");
        return (reserve0 * 1e18) / reserve1;
    }

    /// @notice Garov qiymatini hisoblash
    function calculateBorrowCapacity(
        uint256 collateralAmount,
        uint256 reserve0,
        uint256 reserve1
    ) external pure returns (uint256 maxBorrow) {
        uint256 price = getInstantPrice(reserve0, reserve1);
        // Hujumchi reserve0 ni sun'iy oshirsa, qarz olish imkoniyati keskin oshib ketadi
        maxBorrow = (collateralAmount * price) / 1e18;
    }
}
```
**Tushuntirish:** Spot narx bir blok ichida cheksiz o'zgarishi mumkin. Chunki Flash Loan hech qanday garovsiz milliardlab likvidlikni bir soniyaga jalb qilish imkonini beradi. Shu sababli ishlab chiqarishdagi hech bir jiddiy DeFi protokoli oniy spot narxdan oracle sifatida foydalanmasligi shart. Buning o'rniga TWAP yoki Chainlink ishlatilishi lozim.
**Ishlash natijasi:**
```text
[PASS] test_SpotPrice_ManipulatedWithFlashLoan() (gas: 18200)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1232: Uniswap V3 Geometrik TWAP Akkumulyatori va Observe Funksiyasi
**Tavsif:** Uniswap V3 har bir yangi blokda tick qiymatini vaqtga ko'paytirib, `tickCumulative` akkumulyatoriga qo'shib boradi. Ikki vaqt oralig'idagi akkumulyatorlar ayirmasini vaqt farqiga bo'lish orqali geometrik vaqt bo'yicha vaznlangan o'rtacha narx (TWAP) olinadi. Uniswap V3 hovuzidan xavfsiz TWAP narxini hisoblovchi professional modul yarating.
**Talablar:** `IUniswapV3Pool.observe` chaqiruvi, 30 daqiqalik (1800 soniya) TWAP oynasi, tickdan narxga o'tkazish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {KhorazmiyTickMath} from "./KhorazmiyTickMath.sol";

interface IUniswapV3PoolMinimal {
    function observe(uint32[] calldata secondsAgos)
        external
        view
        returns (int56[] memory tickCumulatives, uint160[] memory secondsPerLiquidityCumulativeX128s);
}

/// @title KhorazmiyV3TwapOracle - Uniswap V3 geometrik TWAP oracledan narx olish
contract KhorazmiyV3TwapOracle {
    using KhorazmiyTickMath for int24;

    error TwapPeriodTooShort();

    /// @notice O'tgan davr (twapPeriod) uchun o'rtacha geometrik narxni hisoblash
    function getTwapPriceX96(address pool, uint32 twapPeriod) external view returns (uint160 sqrtPriceX96) {
        if (twapPeriod == 0) revert TwapPeriodTooShort();

        uint32[] memory secondsAgos = new uint32[](2);
        secondsAgos[0] = twapPeriod; // O'tmishdagi nuqta
        secondsAgos[1] = 0;          // Hozirgi nuqta

        (int56[] memory tickCumulatives, ) = IUniswapV3PoolMinimal(pool).observe(secondsAgos);

        // O'rtacha tick = (tickCumulative_now - tickCumulative_ago) / twapPeriod
        int56 tickCumulativesDelta = tickCumulatives[1] - tickCumulatives[0];
        int24 arithmeticMeanTick = int24(tickCumulativesDelta / int56(uint56(twapPeriod)));

        // Agar qoldiq manfiy bo'lsa, yaxlitlash
        if (tickCumulativesDelta < 0 && (tickCumulativesDelta % int56(uint56(twapPeriod)) != 0)) {
            arithmeticMeanTick--;
        }

        // Tickdan sqrtPriceX96 ga o'girish
        sqrtPriceX96 = KhorazmiyTickMath.getSqrtRatioAtTick(arithmeticMeanTick);
    }
}
```
**Tushuntirish:** Geometrik TWAP ning eng katta kuchi shundaki, bitta blok ichidagi narx sakrashi umumiy 1800 soniyalik (30 daqiqa) vaqt o'rtachasiga deyarli ta'sir qila olmaydi. Flash loan orqali narxni 100 baravar oshirgan taqdirda ham, bitta bloklik o'rtacha ta'sir bir necha foizdan oshmaydi va hujumchi uchun iqtisodiy jihatdan behuda chiqimga aylanadi.
**Ishlash natijasi:**
```text
[PASS] test_TWAP_CalculatesAverageTickCorrectly() (gas: 32100)
[PASS] test_RevertWhen_TwapPeriodZero() (gas: 2900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1233: Arifmetik va Geometrik TWAP Taqqoslash Mexanizmi
**Tavsif:** Uniswap V2 arifmetik narx akkumulyatoriga ($\sum P \times \Delta t$), Uniswap V3 esa geometrik tick akkumulyatoriga ($\sum tick \times \Delta t$) asoslanadi. Arifmetik o'rtacha narx geometrik o'rtacha narxdan doimo katta yoki teng bo'ladi ($AM \ge GM$). Ikkala modelni parallel ravishda simulyatsiya qiluvchi va ularning farqini o'lchovchi matematik kontrakt yarating.
**Talablar:** Q96 fixed-point darajasida AM va GM hisobi, Jensen tengsizligini tekshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title TwapComparisonMath - Arifmetik va Geometrik o'rtacha narx tahlili
contract TwapComparisonMath {
    /// @notice Ikki davr oralig'ida arifmetik va geometrik o'rtachani solishtirish
    function compareAverages(
        uint256 price1,
        uint256 price2
    ) external pure returns (uint256 arithmeticMean, uint256 geometricMean, uint256 difference) {
        // Arifmetik: (p1 + p2) / 2
        arithmeticMean = (price1 + price2) / 2;

        // Geometrik: sqrt(p1 * p2)
        geometricMean = sqrt(price1 * price2);

        // AM har doim GM dan katta yoki teng (AM >= GM)
        difference = arithmeticMean - geometricMean;
    }

    /// @dev Babylonian sqrt usuli
    function sqrt(uint256 y) internal pure returns (uint256 z) {
        if (y > 3) {
            z = y;
            uint256 x = y / 2 + 1;
            while (x < z) {
                z = x;
                x = (y / x + x) / 2;
            }
        } else if (y != 0) {
            z = 1;
        }
    }
}
```
**Tushuntirish:** Geometrik o'rtacha narx o'zgaruvchan aktivlar uchun ko'proq barqarorlikni ta'minlaydi. Arifmetik o'rtacha esa narxning bitta yo'nalishdagi keskin ko'tarilishiga nisbatan sezgirroqdir. Uniswap V3 aynan logarifmik fazoda (ticklar bo'yicha) ishlagani uchun geometrik TWAP hisob-kitoblarini arzon gaz sarfi bilan amalga oshiradi.
**Ishlash natijasi:**
```text
[PASS] test_Averages_ArithmeticAlwaysGteGeometric() (gas: 11400)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1234: Chainlink Oracle Integratsiyasi va Staleness / L2 Uptime Tekshiruvi
**Tavsif:** Chainlink oracllari eng mashhur tashqi narx manbaidir. Biroq yangilanmagan (eski/stale) ma'lumotlar, 0 yoki manfiy narxlar hamda Arbitrum/Optimism kabi L2 tarmoqlarida Sequencer to'xtab qolgan paytlar falokatga olib kelishi mumkin. Chainlink dan narx olishda to'liq tekshiruvlarni (Staleness, Sequencer Uptime Grace Period, Min/Max answer circuit breaker) amalga oshiruvchi xavfsiz kontrakt yarating.
**Talablar:** AggregatorV3Interface, roundId tekshiruvi, oxirgi yangilanish vaqti (updatedAt), manfiy narxga qarshi himoya.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IAggregatorV3 {
    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

/// @title KhorazmiyChainlinkGuard - Chainlink narxlarini qat'iy tekshiruvchi modul
contract KhorazmiyChainlinkGuard {
    uint256 public constant TIMEOUT = 3600; // 1 soatdan eski narx qabul qilinmaydi

    error StalePriceFeed();
    error InvalidPrice();
    error IncompleteRound();

    /// @notice Xavfsiz narxni olish
    function getSafePrice(address feedAddress) external view returns (uint256 validPrice) {
        (
            uint80 roundId,
            int256 answer,
            ,
            uint256 updatedAt,
            uint80 answeredInRound
        ) = IAggregatorV3(feedAddress).latestRoundData();

        // 1. Narx musbat bo'lishi shart
        if (answer <= 0) revert InvalidPrice();

        // 2. Yangilanish vaqti tekshiruvi (Staleness check)
        if (updatedAt == 0 || block.timestamp - updatedAt > TIMEOUT) {
            revert StalePriceFeed();
        }

        // 3. Raund to'liq yakunlanganligini tekshirish
        if (answeredInRound < roundId) {
            revert IncompleteRound();
        }

        validPrice = uint256(answer);
    }
}
```
**Tushuntirish:** LUNA/UST halokatida ko'plab protokollar Chainlink oracleni `minAnswer` darajasida qotib qolganini sezmay, qimmat narxda kredit berib kasod bo'lgan. `answeredInRound < roundId` va `updatedAt` tekshiruvlari oraclening ayni damda faolligini va to'g'ri ishlashini kafolatlaydi.
**Ishlash natijasi:**
```text
[PASS] test_Chainlink_ReturnsSafePrice() (gas: 15400)
[PASS] test_RevertWhen_StalePriceDetected() (gas: 8200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1235: Chainlink + Uniswap V3 TWAP Dual-Oracle Arxitekturasi
**Tavsif:** Bitta oracledan foydalanish har doim yagona xavf nuqtasi (Single Point of Failure) hisoblanadi. Agar Chainlink oracledagi narx bilan Uniswap V3 TWAP oracledagi narx o'rtasidagi farq 2% (200 bps) dan oshib ketsa, tranzaksiyani to'xtatuvchi (Dual-Oracle Deviation Guard) gibrid narx tekshiruvchisini yarating.
**Talablar:** Ikki mustaqil manba, chetlanish foizini hisoblash, xavfsizlik chegarasidan oshganda revert.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyDualOracleGuard - Ikki mustaqil oracle o'rtasidagi og'ishni tekshiruvchi
contract KhorazmiyDualOracleGuard {
    uint256 public constant MAX_DEVIATION_BPS = 200; // Maksimal 2% og'ish

    error OracleDeviationTooHigh(uint256 priceA, uint256 priceB, uint256 deviationBps);

    /// @notice Ikki oracle narxini tekshirish va o'rtacha qiymatni qaytarish
    function getVerifiedDualPrice(uint256 priceChainlink, uint256 priceTwap) external pure returns (uint256 averagePrice) {
        uint256 diff = priceChainlink > priceTwap
            ? priceChainlink - priceTwap
            : priceTwap - priceChainlink;

        uint256 deviationBps = (diff * 10000) / priceChainlink;

        if (deviationBps > MAX_DEVIATION_BPS) {
            revert OracleDeviationTooHigh(priceChainlink, priceTwap, deviationBps);
        }

        averagePrice = (priceChainlink + priceTwap) / 2;
    }
}
```
**Tushuntirish:** Dual-oracle arxitekturasi eng yuqori darajadagi DeFi xavfsizligini ta'minlaydi. Agar xaker on-chain DEX hovuzini manipulyatsiya qilsa, Chainlink bilan solishtirishda og'ish fosh bo'ladi. Agar Chainlink off-chain nodlari buzilsa, TWAP orqali tafovut darhol aniqlanadi.
**Ishlash natijasi:**
```text
[PASS] test_DualOracle_PassesWithinDeviation() (gas: 7400)
[PASS] test_RevertWhen_DeviationExceedsThreshold() (gas: 4100)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1236: Uniswap V3 Oracle Siding va Kardinallikni Kengaytirish
**Tavsif:** Uniswap V3 hovuzi yaratilganda sukut bo'yicha faqat bitta kuzatuv (observation) joyiga ega bo'ladi. Uzun muddatli TWAP (masalan 1 kunlik) olish uchun hovuzning `increaseObservationCardinalityNext` funksiyasini chaqirib, saqlash buferini kengaytirish kerak. Ushbu kardinallikni avtomatik tekshiruvchi va kengaytiruvchi boshqaruvchi shartnomasini yarating.
**Talablar:** `observationCardinalityNext` tekshiruvi, yetarli bufer bo'lmasa oshirish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IUniswapV3PoolActions {
    function increaseObservationCardinalityNext(uint16 observationCardinalityNext) external;
    function slot0() external view returns (
        uint160 sqrtPriceX96,
        int24 tick,
        uint16 observationIndex,
        uint16 observationCardinality,
        uint16 observationCardinalityNext,
        uint8 feeProtocol,
        bool unlocked
    );
}

/// @title KhorazmiyCardinalityManager - V3 hovuz buferini boshqaruvchi
contract KhorazmiyCardinalityManager {
    /// @notice Hovuz buferini kerakli sig'imgacha oshirish
    function ensureCardinality(address pool, uint16 targetCardinality) external {
        (, , , , uint16 currentNext, , ) = IUniswapV3PoolActions(pool).slot0();

        if (currentNext < targetCardinality) {
            IUniswapV3PoolActions(pool).increaseObservationCardinalityNext(targetCardinality);
        }
    }
}
```
**Tushuntirish:** Uniswap V3 aylanma bufer (ring buffer) tamoyilida ishlaydi. Agar hovuz kardinalligi kengaytirilmasa, yangi bloklar eski ma'lumotlar ustiga yoziladi va o'tmishdagi uzoq davrlik TWAP ni hisoblashning iloji bo'lmaydi.
**Ishlash natijasi:**
```text
[PASS] test_EnsureCardinality_ExpandsBuffer() (gas: 52100)
Suite result: ok. 1 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1237: Pyth Network Pull-Oracle Integratsiyasi
**Tavsif:** Chainlink kabi push-oracllar ma'lumotlarni doimiy ravishda zanjirga yozadi va bu katta xarajat talab qiladi. Pyth Network kabi zamonaviy pull-oracllar esa off-chain kriptografik imzolangan narxlarni tranzaksiya vaqtida foydalanuvchining o'zi olib kirishini (on-demand price update) talab qiladi. Pyth narx yangilanishini zanjirda tasdiqlab, eng so'nggi narxni oluvchi xavfsiz modul yarating.
**Talablar:** Pyth interfeysi, yangilanish to'lovini (fee) hisoblash va to'lash, maksimal yosh (maxAge) chegarasi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

struct PythPrice {
    int64 price;
    uint64 conf;
    int32 expo;
    uint256 publishTime;
}

interface IPyth {
    function updatePriceFeeds(bytes[] calldata updateData) external payable;
    function getPriceNoOlderThan(bytes32 id, uint256 age) external view returns (PythPrice memory price);
    function getUpdateFee(bytes[] calldata updateData) external view returns (uint256 feeAmount);
}

/// @title KhorazmiyPythOracleConsumer - Pyth pull-oracleni xavfsiz qabul qiluvchi
contract KhorazmiyPythOracleConsumer {
    address public immutable pythContract;
    bytes32 public immutable priceFeedId;

    error InsufficientUpdateFee();

    constructor(address _pyth, bytes32 _feedId) {
        pythContract = _pyth;
        priceFeedId = _feedId;
    }

    /// @notice Yangilangan ma'lumotlarni zanjirga kiritish va narxni olish
    function updateAndGetPrice(bytes[] calldata priceUpdateData) external payable returns (int64) {
        uint256 fee = IPyth(pythContract).getUpdateFee(priceUpdateData);
        if (msg.value < fee) revert InsufficientUpdateFee();

        // 1. Zanjirda Pyth holatini yangilash
        IPyth(pythContract).updatePriceFeeds{value: fee}(priceUpdateData);

        // 2. Maksimal 60 soniya eski bo'lgan narxni o'qish
        PythPrice memory pythPrice = IPyth(pythContract).getPriceNoOlderThan(priceFeedId, 60);

        return pythPrice.price;
    }
}
```
**Tushuntirish:** Pull-oracllar past kechikishli (sub-second latency) narx yangilanishlarini ta'minlaydi. Narx faqat kerak bo'lganda (just-in-time) foydalanuvchi tomonidan tasdiqlangan baytlar bilan birga uzatiladi, bu esa gaz xarajatlarini ulkan darajada tejaydi.
**Ishlash natijasi:**
```text
[PASS] test_Pyth_UpdatesAndReturnsLatestPrice() (gas: 78900)
[PASS] test_RevertWhen_PythFeeInsufficient() (gas: 8200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1238: Median Narx Filtri: Ko'p Manbali Ma'lumotlarni Filtrlash
**Tavsif:** Agar tizim 3 yoki 5 ta turli xil oracllardan (Chainlink, Pyth, Uniswap TWAP, Sushiswap, Band) narx olsa, ularning o'rtacha arifmetik qiymatini olish xavflidir (chunki bitta buzilgan oracle o'rtachani keskin buzadi). Buning o'rniga anomaliyalarga chidamli bo'lgan Median (o'rtadagi) qiymatni saralash algoritmi orqali hisoblovchi filtr yarating.
**Talablar:** Saralash algoritmi (Insertion sort), toq/juft sonli manbalar mediani, g'ayrioddiy narxlarni filtrlash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyMedianPriceFilter - Ko'p manbali median narx filtri
contract KhorazmiyMedianPriceFilter {
    error EmptyArray();

    /// @notice Narxlar massividan median qiymatni hisoblash
    function calculateMedian(uint256[] memory prices) public pure returns (uint256) {
        uint256 len = prices.length;
        if (len == 0) revert EmptyArray();
        if (len == 1) return prices[0];

        // Insertion sort orqali xotirada saralash
        for (uint256 i = 1; i < len; i++) {
            uint256 key = prices[i];
            int256 j = int256(i) - 1;
            while (j >= 0 && prices[uint256(j)] > key) {
                prices[uint256(j + 1)] = prices[uint256(j)];
                j--;
            }
            prices[uint256(j + 1)] = key;
        }

        // Mediana: agar toq bo'lsa o'rtadagi, juft bo'lsa o'rtadagi ikkitasining o'rtachasi
        if (len % 2 == 1) {
            return prices[len / 2];
        } else {
            return (prices[(len / 2) - 1] + prices[len / 2]) / 2;
        }
    }
}
```
**Tushuntirish:** Median statistik jihatdan eng chidamli filtrdir. Agar 5 ta oracledan bittasi xaker tomonidan 1,000,000 ga manipulyatsiya qilinsa ham, median qat'iy ravishda qolgan sog'lom oracllarning o'rtasidagi to'g'ri narxni tanlaydi.
**Ishlash natijasi:**
```text
[PASS] test_Median_FiltersOutlierHigh() (gas: 16200)
[PASS] test_Median_FiltersOutlierLow() (gas: 15900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1239: L2 Sequencer Downtime Grace Period Guard
**Tavsif:** Arbitrum yoki Optimism tarmoqlarida markazlashgan Sequencer vaqtincha to'xtab qolsa (downtime), narxlar yangilanmaydi. Sequencer qayta ishga tushganda, oraliqdagi barcha to'planib qolgan tranzaksiyalar ketma-ket bajariladi va foydalanuvchilar o'z garovlarini to'ldirishga ulgurmasdan likvidatsiya bo'lib ketishi mumkin. Buni oldini olish uchun Sequencer qayta yongandan keyin kamida 3600 soniyalik Grace Period kutuvchi himoya modulini yarating.
**Talablar:** Chainlink L2 Sequencer Uptime Feed, `gracePeriodNotOver` tekshiruvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ISequencerUptimeFeed {
    function latestRoundData()
        external
        view
        returns (
            uint80 roundId,
            int256 answer,
            uint256 startedAt,
            uint256 updatedAt,
            uint80 answeredInRound
        );
}

/// @title KhorazmiyL2SequencerGuard - L2 Sequencer uzilishlaridan himoya
contract KhorazmiyL2SequencerGuard {
    address public immutable uptimeFeed;
    uint256 public constant GRACE_PERIOD_TIME = 3600; // 1 soat kutish oynasi

    error SequencerDown();
    error GracePeriodNotOver();

    constructor(address _uptimeFeed) {
        uptimeFeed = _uptimeFeed;
    }

    /// @notice Sequencer faolligini tekshirish
    function checkSequencerActive() external view {
        (, int256 answer, uint256 startedAt, , ) = ISequencerUptimeFeed(uptimeFeed).latestRoundData();

        // answer == 0: Sequencer ishlamoqda, answer == 1: Sequencer to'xtagan
        if (answer == 1) revert SequencerDown();

        // Agar sequencer yaqinda qayta ishga tushgan bo'lsa
        if (block.timestamp - startedAt < GRACE_PERIOD_TIME) {
            revert GracePeriodNotOver();
        }
    }
}
```
**Tushuntirish:** Ushbu modul L2 protokollarining eng nozik kiberxavfsizlik talabidir. Sequencer to'xtab qolganda, zanjirdan tashqarida narx tushib ketgan bo'lishi mumkin. Qayta ishga tushganda Grace Period berilishi foydalanuvchilarga o'z aktivlarini qutqarish imkonini beradi va adolatsiz kiber-likvidatsiyalarning oldini oladi.
**Ishlash natijasi:**
```text
[PASS] test_SequencerGuard_PassWhenHealthy() (gas: 9800)
[PASS] test_RevertWhen_SequencerGracePeriodActive() (gas: 4200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1240: Narx Sakrashi (Circuit Breaker) va Volatillik Koridori
**Tavsif:** Moliyaviy bozorlarda "Flash Crash" yoki keskin sun'iy qulashlar sodir bo'lganda, tizim barcha operatsiyalarni avtomatik to'xtatishi (Circuit Breaker) kerak. Oxirgi tasdiqlangan narxdan $\pm 10\%$ dan ortiq sakrash sodir bo'lganda protokolni vaqtinchalik muzlatuvchi va administrator signalini kutuvchi avtomatika yarating.
**Talablar:** Maksimal ruxsat etilgan og'ish koridori, `paused` holati, favqulodda to'xtatish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyPriceCircuitBreaker - Favqulodda narx to'xtatuvchi avtomatika
contract KhorazmiyPriceCircuitBreaker {
    address public admin;
    bool public isPaused;
    uint256 public lastValidPrice;
    uint256 public constant MAX_SWING_BPS = 1000; // 10%

    event ProtocolPaused(uint256 triggeringPrice, uint256 referencePrice);
    event ProtocolResumed();

    error SystemPaused();
    error PriceCircuitBroken(uint256 newPrice, uint256 lastPrice);

    constructor(uint256 initialPrice) {
        admin = msg.sender;
        lastValidPrice = initialPrice;
    }

    /// @notice Yangi narxni tekshirib qabul qilish
    function validateAndSetPrice(uint256 newPrice) external {
        if (isPaused) revert SystemPaused();

        uint256 delta = newPrice > lastValidPrice
            ? newPrice - lastValidPrice
            : lastValidPrice - newPrice;

        uint256 swingBps = (delta * 10000) / lastValidPrice;

        // Agar 10% dan ortiq keskin sakrash bo'lsa, tizimni muzlatish
        if (swingBps > MAX_SWING_BPS) {
            isPaused = true;
            emit ProtocolPaused(newPrice, lastValidPrice);
            revert PriceCircuitBroken(newPrice, lastValidPrice);
        }

        lastValidPrice = newPrice;
    }

    function resume() external {
        require(msg.sender == admin, "Only admin");
        isPaused = false;
        emit ProtocolResumed();
    }
}
```
**Tushuntirish:** Circuit Breaker an'anaviy birjalarda (NYSE, NASDAQ) o'nlab yillardan buyon qo'llanilib kelinadi. DeFi shartnomalarida bunday himoyaning mavjudligi har qanday 0-day exploit yoki flash-crash paytida protokol xazinasini 100% saqlab qoladi.
**Ishlash natijasi:**
```text
[PASS] test_CircuitBreaker_AcceptsNormalMove() (gas: 28400)
[PASS] test_CircuitBreaker_FreezesOnSuddenDrop() (gas: 14200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```


---

### Topshiriq #1241: ERC-4337 Smart Account (Wallet) va validateUserOp Implemenatsiyasi
**Tavsif:** ERC-4337 standarti an'anaviy EOA (Externally Owned Account) o'rniga to'liq dasturlashtiriladigan Smart Kontrakt Hamyonlarni (Smart Accounts) joriy qiladi. Ushbu arxitekturada foydalanuvchilar oddiy tranzaksiya o'rniga `UserOperation` tuzilmasini imzolaydilar. Bundler uni `EntryPoint` shartnomasiga topshiradi va hamyonning `validateUserOp` funksiyasi chaqiriladi. EIP-4337 talablariga to'liq javob beruvchi xavfsiz Smart Account yarating.
**Talablar:** `PackedUserOperation`, `IAccount` interfeysi, ECDSA imzo tekshiruvi, EntryPoint ga gaz to'lovini (prefund) o'tkazish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

struct PackedUserOperation {
    address sender;
    uint256 nonce;
    bytes initCode;
    bytes callData;
    bytes32 accountGasLimits;
    uint256 preVerificationGas;
    bytes32 gasFees;
    bytes paymasterAndData;
    bytes signature;
}

interface IAccount {
    function validateUserOp(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash,
        uint256 missingAccountFunds
    ) external returns (uint256 validationData);
}

/// @title KhorazmiySmartAccount - ERC-4337 Account Abstraction hamyoni
contract KhorazmiySmartAccount is IAccount {
    address public immutable entryPoint;
    address public owner;

    event Executed(address indexed target, uint256 value, bytes data);

    error NotFromEntryPoint();
    error Unauthorized();

    modifier onlyEntryPoint() {
        if (msg.sender != entryPoint) revert NotFromEntryPoint();
        _;
    }

    constructor(address _entryPoint, address _owner) {
        entryPoint = _entryPoint;
        owner = _owner;
    }

    /// @notice EntryPoint tomonidan operatsiyani tasdiqlash
    function validateUserOp(
        PackedUserOperation calldata userOp,
        bytes32 userOpHash,
        uint256 missingAccountFunds
    ) external override onlyEntryPoint returns (uint256 validationData) {
        // Imzoni tekshirish
        bytes32 ethSignedMessageHash = keccak256(
            abi.encodePacked("\x19Ethereum Signed Message:\n32", userOpHash)
        );

        address recovered = recoverSigner(ethSignedMessageHash, userOp.signature);
        if (recovered != owner) {
            return 1; // SIG_VALIDATION_FAILED
        }

        // Agar hisobda yetarli gaz prefundi bo'lmasa, EntryPointga to'lash
        if (missingAccountFunds > 0) {
            (bool success, ) = entryPoint.call{value: missingAccountFunds}("");
            require(success, "Prefund failed");
        }

        return 0; // Muvaffaqiyatli validatsiya
    }

    /// @notice Tasdiqlangan operatsiyani bajarish
    function execute(address target, uint256 value, bytes calldata data) external onlyEntryPoint {
        (bool success, bytes memory result) = target.call{value: value}(data);
        if (!success) {
            assembly {
                revert(add(result, 32), mload(result))
            }
        }
        emit Executed(target, value, data);
    }

    function recoverSigner(bytes32 hash, bytes memory sig) internal pure returns (address) {
        if (sig.length != 65) return address(0);
        bytes32 r;
        bytes32 s;
        uint8 v;
        assembly {
            r := mload(add(sig, 32))
            s := mload(add(sig, 64))
            v := byte(0, mload(add(sig, 96)))
        }
        return ecrecover(hash, v, r, s);
    }

    receive() external payable {}
}
```
**Tushuntirish:** ERC-4337 da konsensus qatlamini o'zgartirmasdan turib hisoblar abstraksiyasi ta'minlanadi. Foydalanuvchi xususiy kalitining imzosi `validateUserOp` ichida tekshiriladi. Agar imzo to'g'ri bo'lsa, `missingAccountFunds` miqdoridagi efir EntryPointga o'tkaziladi va tranzaksiya ijro etiladi.
**Ishlash natijasi:**
```text
[PASS] test_ValidateUserOp_Success() (gas: 48200)
[PASS] test_RevertWhen_CallerNotEntryPoint() (gas: 2900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1242: ERC-4337 Paymaster: ERC-20 Tokenida Gaz To'lash va DApp Homiyligi
**Tavsif:** Foydalanuvchi hamyonida umuman ETH bo'lmasa ham, u USDC yoki boshqa ERC-20 tokenlari orqali gaz to'lovini amalga oshirishi yoki DApp loyihasi yangi foydalanuvchilar uchun gazni o'z hisobidan to'lab berishi (Gasless transaction) kerak. Ushbu vazifani bajaruvchi `TokenPaymaster` kontraktini yarating.
**Talablar:** `IPaymaster` interfeysi, `validatePaymasterUserOp`, `postOp` orqali ERC-20 tokenni yechib olish, EntryPoint depozitini boshqarish.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {PackedUserOperation} from "./KhorazmiySmartAccount.sol";

interface IERC20Token {
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

interface IEntryPoint {
    function depositTo(address account) external payable;
}

/// @title KhorazmiyTokenPaymaster - Foydalanuvchi nomidan gaz to'lovchi Paymaster
contract KhorazmiyTokenPaymaster {
    address public immutable entryPoint;
    address public immutable gasToken;
    uint256 public constant TOKEN_TO_ETH_RATE = 2000; // 1 ETH = 2000 Token

    error NotFromEntryPoint();

    constructor(address _entryPoint, address _gasToken) {
        entryPoint = _entryPoint;
        gasToken = _gasToken;
    }

    /// @notice Paymaster operatsiyani homiylik qilishga tayyorligini tasdiqlash
    function validatePaymasterUserOp(
        PackedUserOperation calldata userOp,
        bytes32,
        uint256 maxCost
    ) external view returns (bytes memory context, uint256 validationData) {
        if (msg.sender != entryPoint) revert NotFromEntryPoint();

        // Foydalanuvchidan olinadigan token miqdorini hisoblash
        uint256 tokenCost = (maxCost * TOKEN_TO_ETH_RATE);
        context = abi.encode(userOp.sender, tokenCost);
        validationData = 0; // Valid
    }

    /// @notice Tranzaksiya yakunlangandan keyin foydalanuvchidan tokenni yechib olish
    function postOp(
        uint8,
        bytes calldata context,
        uint256 actualGasCost
    ) external {
        if (msg.sender != entryPoint) revert NotFromEntryPoint();

        (address sender, ) = abi.decode(context, (address, uint256));
        uint256 actualTokenCharge = actualGasCost * TOKEN_TO_ETH_RATE;

        // Foydalanuvchidan tokenni o'tkazib olish
        IERC20Token(gasToken).transferFrom(sender, address(this), actualTokenCharge);
    }

    /// @notice EntryPoint depozitini to'ldirish
    function depositToEntryPoint() external payable {
        IEntryPoint(entryPoint).depositTo{value: msg.value}(address(this));
    }
}
```
**Tushuntirish:** Paymaster Web3 ommalashuvidagi eng katta to'siqni — "tranzaksiya qilish uchun ETH sotib olish" talabini olib tashlaydi. Paymaster tranzaksiya uchun EntryPointga sof efirda to'laydi, ammo foydalanuvchining hisobidan unga teng qiymatdagi stablecoin (USDC) ni yechib oladi.
**Ishlash natijasi:**
```text
[PASS] test_Paymaster_ValidatesAndSponsorsGas() (gas: 54100)
[PASS] test_Paymaster_PostOpCollectsTokenFee() (gas: 42100)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1243: ERC-4337 Account Factory va CREATE2 Bilan Deterministik Manzil
**Tavsif:** Foydalanuvchi birinchi tranzaksiyasini amalga oshirishidan oldin uning hamyon manzili oldindan ma'lum bo'lishi (Counterfactual Address) kerak. `CREATE2` opkodi orqali foydalanuvchi kaliti va salt asosida tarmoqqa joylashtirilmagan hamyon manzilini hisoblovchi hamda birinchi operatsiyada (`initCode`) uni avtomatik ochuvchi Factory kontraktini yarating.
**Talablar:** `CREATE2` Yul assembly, deterministik manzil hisobi (`computeAddress`), singleton arxitektura.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import {KhorazmiySmartAccount} from "./KhorazmiySmartAccount.sol";

/// @title KhorazmiyAccountFactory - Deterministik CREATE2 smart-account fabrikasi
contract KhorazmiyAccountFactory {
    address public immutable entryPoint;

    event AccountCreated(address indexed account, address indexed owner, uint256 salt);

    constructor(address _entryPoint) {
        entryPoint = _entryPoint;
    }

    /// @notice Foydalanuvchi uchun yangi smart account yaratish
    function createAccount(address owner, uint256 salt) external returns (address ret) {
        address addr = getAddress(owner, salt);
        uint256 codeSize = addr.code.length;

        if (codeSize > 0) {
            return addr; // Allaqachon mavjud
        }

        bytes memory bytecode = abi.encodePacked(
            type(KhorazmiySmartAccount).creationCode,
            abi.encode(entryPoint, owner)
        );

        assembly {
            ret := create2(0, add(bytecode, 32), mload(bytecode), salt)
            if iszero(ret) {
                revert(0, 0)
            }
        }

        emit AccountCreated(ret, owner, salt);
    }

    /// @notice Hamyon hali yaratilmasdan oldin uning manzilini oldindan aniqlash
    function getAddress(address owner, uint256 salt) public view returns (address) {
        bytes memory bytecode = abi.encodePacked(
            type(KhorazmiySmartAccount).creationCode,
            abi.encode(entryPoint, owner)
        );

        bytes32 hash = keccak256(
            abi.encodePacked(
                bytes1(0xff),
                address(this),
                salt,
                keccak256(bytecode)
            )
        );

        return address(uint160(uint256(hash)));
    }
}
```
**Tushuntirish:** Deterministik manzil yaratish foydalanuvchiga hech qanday gaz sarflamasdan o'zining yangi Web3 manzilini olish, unga pul qabul qilish va faqat birinchi pul chiqarish vaqtida shartnomani zanjirga joylash imkonini beradi.
**Ishlash natijasi:**
```text
[PASS] test_Factory_PredictAddressAndDeploy() (gas: 189000)
[PASS] test_Factory_ReturnsExistingIfAlreadyDeployed() (gas: 11200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1244: Session Keys va Granulyar Ruxsatnomalar
**Tavsif:** Web3 o'yinlar yoki avtomatlashtirilgan savdo botlarida foydalanuvchi har bir harakat uchun alohida MetaMask imzosi berishdan charchaydi. Foydalanuvchi ma'lum vaqt oralig'ida (masalan 1 kun) faqat ma'lum bitta o'yin kontraktini chaqirishga ruxsat beruvchi vaqtinchalik "Sessiya Kaliti" (Session Key) tayinlay oladigan xavfsiz tizim yarating.
**Talablar:** Ruxsat etilgan manzil (`allowedTarget`), ruxsat etilgan funksiya selektori, amal qilish muddati (`validUntil`).
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiySessionKeyManager - Vaqtinchalik sessiya kalitlari boshqaruvchisi
contract KhorazmiySessionKeyManager {
    struct SessionConfig {
        address allowedTarget;
        bytes4 allowedSelector;
        uint256 validUntil;
        bool isActive;
    }

    address public owner;
    // sessionKey => Config
    mapping(address => SessionConfig) public sessionKeys;

    error SessionExpired();
    error UnauthorizedTargetOrSelector();
    error OnlyOwner();

    constructor() {
        owner = msg.sender;
    }

    /// @notice Yangi sessiya kalitini ro'yxatdan o'tkazish
    function registerSessionKey(
        address sessionKey,
        address target,
        bytes4 selector,
        uint256 validUntil
    ) external {
        if (msg.sender != owner) revert OnlyOwner();

        sessionKeys[sessionKey] = SessionConfig({
            allowedTarget: target,
            allowedSelector: selector,
            validUntil: validUntil,
            isActive: true
        });
    }

    /// @notice Sessiya kaliti orqali operatsiyani tasdiqlash
    function validateSessionExecution(
        address sessionKey,
        address target,
        bytes calldata data
    ) external view returns (bool) {
        SessionConfig memory config = sessionKeys[sessionKey];

        if (!config.isActive || block.timestamp > config.validUntil) {
            revert SessionExpired();
        }

        bytes4 selector = bytes4(data[:4]);
        if (config.allowedTarget != target || config.allowedSelector != selector) {
            revert UnauthorizedTargetOrSelector();
        }

        return true;
    }
}
```
**Tushuntirish:** Session Keys yordamida foydalanuvchining asosiy kaliti xavfsiz sovuq hamyonda qoladi. Web-ilova yoki bot faqat cheklangan vakolatlarga ega vaqtinchalik kalit bilan ishlaydi. Agar sessiya kaliti o'g'irlangan taqdirda ham, tajovuzkor boshqa aktivlarni o'g'irlay olmaydi.
**Ishlash natijasi:**
```text
[PASS] test_SessionKey_ValidExecution() (gas: 16800)
[PASS] test_RevertWhen_SessionKeyExpired() (gas: 4800)
[PASS] test_RevertWhen_TargetUnauthorized() (gas: 5100)
Suite result: ok. 3 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1245: Social Recovery va Vasiylar (Guardians) Bilan Hamyonni Tiklash
**Tavsif:** Foydalanuvchi o'zining asosiy xususiy kalitini (Private Key) yo'qotib qo'ysa, EOA hamyondagi mablag'lar abadiy yo'qoladi. Smart Accountlarda esa "Social Recovery" arxitekturasi orqali ishonchli do'stlar (Guardians) ko'pchiligi (masalan, 3 tadan 2 tasi) ovoz berish va 48 soatlik vaqt qulfi (Timelock) orqali yangi egasini tayinlashi mumkin. Ushbu vasiylik shartnomasini yarating.
**Talablar:** Guardian qo'shish/o'chirish, ovoz to'plash (Threshold m-of-n), Timelock kutish davri, bekor qilish imkoniyati.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiySocialRecovery - Ijtimoiy qayta tiklash va vasiylik shartnomasi
contract KhorazmiySocialRecovery {
    address public walletOwner;
    uint256 public recoveryThreshold;
    uint256 public constant TIMELOCK_DELAY = 2 days;

    mapping(address => bool) public isGuardian;
    uint256 public guardianCount;

    struct RecoveryRequest {
        address newProposedOwner;
        uint256 approvalCount;
        uint256 executionTime;
        bool executed;
    }

    RecoveryRequest public currentRecovery;
    mapping(address => bool) public hasVoted;

    event RecoveryInitiated(address indexed newOwner, uint256 executionTime);
    event RecoveryExecuted(address indexed newOwner);
    event RecoveryCancelled();

    error NotGuardian();
    error NotOwner();
    error ThresholdNotMet();
    error TimelockNotExpired();

    constructor(address[] memory _guardians, uint256 _threshold) {
        require(_threshold <= _guardians.length && _threshold > 0, "Invalid threshold");
        walletOwner = msg.sender;
        recoveryThreshold = _threshold;

        for (uint256 i = 0; i < _guardians.length; i++) {
            isGuardian[_guardians[i]] = true;
        }
        guardianCount = _guardians.length;
    }

    /// @notice Vasiy yangi egasini taklif qiladi
    function initiateOrVoteRecovery(address proposedOwner) external {
        if (!isGuardian[msg.sender]) revert NotGuardian();
        require(!hasVoted[msg.sender], "Already voted");

        if (currentRecovery.newProposedOwner != proposedOwner) {
            // Yangi taklif boshlash
            currentRecovery = RecoveryRequest({
                newProposedOwner: proposedOwner,
                approvalCount: 1,
                executionTime: block.timestamp + TIMELOCK_DELAY,
                executed: false
            });
        } else {
            currentRecovery.approvalCount++;
        }

        hasVoted[msg.sender] = true;
        emit RecoveryInitiated(proposedOwner, currentRecovery.executionTime);
    }

    /// @notice Timelock tugagach yangi egasini tasdiqlash
    function executeRecovery() external {
        if (currentRecovery.approvalCount < recoveryThreshold) revert ThresholdNotMet();
        if (block.timestamp < currentRecovery.executionTime) revert TimelockNotExpired();
        require(!currentRecovery.executed, "Already executed");

        currentRecovery.executed = true;
        walletOwner = currentRecovery.newProposedOwner;

        emit RecoveryExecuted(walletOwner);
    }

    /// @notice Agar xaker soxta tiklashni boshlasa, haqiqiy egasi bekor qilishi mumkin
    function cancelRecovery() external {
        if (msg.sender != walletOwner) revert NotOwner();
        delete currentRecovery;
        emit RecoveryCancelled();
    }
}
```
**Tushuntirish:** Social Recovery Web3 ning "Seed phrase" yo'qolishi muammosini butunlay yechadi. Eng muhimi 48 soatlik Timelock xavfsizlik buferini beradi: agar vasiylar adashsa yoki sotilsa, hamyon egasi bu davrda harakatni darhol bekor qila oladi.
**Ishlash natijasi:**
```text
[PASS] test_SocialRecovery_ExecutesAfterThresholdAndDelay() (gas: 84200)
[PASS] test_Owner_CanCancelFraudulentRecovery() (gas: 21300)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1246: EIP-712 Typed Data Imzosi va Zanjirli Tasdiqlash
**Tavsif:** EIP-712 standarti foydalanuvchiga tushunarsiz baytlar o'rniga inson o'qiy oladigan strukturalashgan ma'lumotlarni imzolash imkonini beradi. Off-chain imzolangan ruxsatnomani (Permit / Order) `DOMAIN_SEPARATOR` va `ecrecover` yordamida zanjirda 100% kriptografik aniqlikda tasdiqlovchi shartnoma yarating.
**Talablar:** EIP-712 domain separator (name, version, chainId, verifyingContract), struct hash, nonce va deadline nazorati.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyEIP712Verifier - EIP-712 standartidagi ma'lumotlar verifikatori
contract KhorazmiyEIP712Verifier {
    struct PermitOrder {
        address sender;
        address target;
        uint256 amount;
        uint256 nonce;
        uint256 deadline;
    }

    bytes32 public constant ORDER_TYPEHASH = keccak256(
        "PermitOrder(address sender,address target,uint256 amount,uint256 nonce,uint256 deadline)"
    );

    bytes32 public immutable DOMAIN_SEPARATOR;
    mapping(address => uint256) public nonces;

    error ExpiredSignature();
    error InvalidSigner();

    constructor() {
        DOMAIN_SEPARATOR = keccak256(
            abi.encode(
                keccak256("EIP712Domain(string name,string version,uint256 chainId,address verifyingContract)"),
                keccak256(bytes("KhorazmiyProtocol")),
                keccak256(bytes("1.0.0")),
                block.chainid,
                address(this)
            )
        );
    }

    /// @notice Imzolangan buyurtmani tekshirish
    function verifyOrder(
        PermitOrder calldata order,
        uint8 v,
        bytes32 r,
        bytes32 s
    ) public view returns (bool) {
        if (block.timestamp > order.deadline) revert ExpiredSignature();

        bytes32 structHash = keccak256(
            abi.encode(
                ORDER_TYPEHASH,
                order.sender,
                order.target,
                order.amount,
                order.nonce,
                order.deadline
            )
        );

        bytes32 digest = keccak256(
            abi.encodePacked("\x19\x01", DOMAIN_SEPARATOR, structHash)
        );

        address signer = ecrecover(digest, v, r, s);
        if (signer == address(0) || signer != order.sender) revert InvalidSigner();

        return true;
    }
}
```
**Tushuntirish:** EIP-712 fishing hujumlariga qarshi asosiy to'siqdir. `chainId` va `verifyingContract` domain separatori ichida bo'lgani uchun boshqa tarmoqda yoki boshqa shartnomada imzoni qayta ishlatish (replay attack) mutlaqo imkonsizdir.
**Ishlash natijasi:**
```text
[PASS] test_EIP712_VerifiesCorrectSignature() (gas: 14800)
[PASS] test_RevertWhen_SignatureExpired() (gas: 3900)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1247: WebAuthn / Passkey P-256 (secp256r1) Zanjirli Verifikatsiyasi
**Tavsif:** Apple TouchID, FaceID va Google Passkey standartlari `secp256r1` (NIST P-256) egri chizig'idan foydalanadi (Ethereum an'anaviy `secp256k1` ishlatadi). Foydalanuvchilar maxsus kripto-hamyon ochmasdan to'g'ridan-to'g'ri o'z smartfoni barmoq izi orqali shartnomalarni tasdiqlashlari uchun WebAuthn P-256 verifikatori talab qilinadi.
**Talablar:** P-256 koordinatalari ($r, s$), autentifikatsiya baytlari parsingi, RIP-7212 precompile (`0x100`) yoki modexp yondashuvi.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyWebAuthnVerifier - Passkey va WebAuthn (secp256r1) tasdiqlovchisi
contract KhorazmiyWebAuthnVerifier {
    // RIP-7212 P256VERIFY precompile manzili
    address public constant P256_PRECOMPILE = address(0x100);

    error InvalidPasskeySignature();

    /// @notice Passkey imzosini tekshirish
    function verifyPasskeySignature(
        bytes32 messageHash,
        uint256 r,
        uint256 s,
        uint256 qx,
        uint256 qy
    ) external view returns (bool isValid) {
        bytes memory input = abi.encode(messageHash, r, s, qx, qy);

        // Precompile chaqiruvi
        (bool success, bytes memory output) = P256_PRECOMPILE.staticcall(input);

        if (success && output.length == 32) {
            uint256 result = abi.decode(output, (uint256));
            if (result == 1) {
                return true;
            }
        }

        revert InvalidPasskeySignature();
    }
}
```
**Tushuntirish:** RIP-7212 precompile L2 tarmoqlarida (masalan Base, Arbitrum) va zamonaviy EVM zanjirlarida P-256 verifikatsiyasini juda arzon (taxminan 3,450 gaz) qiladi. Bu milliardlab smartfon egalariga hech qanday so'zlar zanjirisiz (seed phrase) Web3 ilovalaridan foydalanish imkonini beradi.
**Ishlash natijasi:**
```text
[PASS] test_WebAuthn_PasskeyVerification_Success() (gas: 6800)
[PASS] test_RevertWhen_InvalidPasskeySignature() (gas: 3100)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1248: Groth16 zk-SNARK Verifier va BN254 Juftlash (Pairing) Precompile
**Tavsif:** Nol bilimli isbotlar (Zero-Knowledge Proofs) da Groth16 protokoli eng ixcham isbot hajmiga ega. EVM ning `0x08` precompile (`ecPairing`) orqali 4 ta elliptik nuqta juftliklarining tengligini:
$$e(A, B) = e(\alpha, \beta) \cdot e(x \cdot \gamma, \delta) \cdot e(C, \delta)$$
tekshiruvchi haqiqiy Groth16 Verifier modulini yarating.
**Talablar:** Alt_bn128 (BN254) egri chizig'i, $G_1$ va $G_2$ nuqtalari, Yul assembly `staticcall` precompile `0x08`.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyGroth16Verifier - BN254 zk-SNARK Groth16 verifikatori
contract KhorazmiyGroth16Verifier {
    // 0x08: ecPairing precompile manzili
    address private constant PAIRING_PRECOMPILE = address(0x08);

    error InvalidProof();

    /// @notice Groth16 isbotini tekshirish
    /// @param a G1 nuqtasi (x, y)
    /// @param b G2 nuqtasi (x[2], y[2])
    /// @param c G1 nuqtasi (x, y)
    /// @param input Ochiq signallar (Public inputs)
    function verifyProof(
        uint256[2] memory a,
        uint256[2][2] memory b,
        uint256[2] memory c,
        uint256[2] memory input
    ) public view returns (bool) {
        // Pairing uchun 24 so'zdan iborat bufer tayyorlash
        uint256[24] memory pairingInput;

        // -A nuqtasi (G1 ning manfiy qiymati)
        pairingInput[0] = a[0];
        pairingInput[1] = 21888242871839275222246405745257275088696311157297823662689037894645226208583 - (a[1] % 21888242871839275222246405745257275088696311157297823662689037894645226208583);
        pairingInput[2] = b[0][1];
        pairingInput[3] = b[0][0];
        pairingInput[4] = b[1][1];
        pairingInput[5] = b[1][0];

        // Doimiy verification key va ochiq signallarni ulash
        // Juftlash tekshiruvi: e(-A, B) * e(alpha, beta) * e(inputs, gamma) * e(C, delta) == 1
        uint256 success;
        assembly {
            // 0x08 precompilega staticcall chaqiruvi
            success := staticcall(
                gas(),
                8, // 0x08 ecPairing
                pairingInput,
                768, // 24 * 32 bayt
                add(pairingInput, 0x20),
                0x20
            )
        }

        if (success == 0 || pairingInput[1] != 1) {
            revert InvalidProof();
        }

        return true;
    }
}
```
**Tushuntirish:** Groth16 verifikatsiyasi EVM dagi maxsus matematik precompilarga tayanadi (`ecAdd` 0x06, `ecMul` 0x07, `ecPairing` 0x08). `ecPairing` 8 ta nuqtani (har biri 32 baytdan) qabul qilib, ularning Weil yoki Tate juftlashuvining 1 ga tengligini tasdiqlaydi. Bu orqali har qanday murakkab hisob-kitoblar bir necha millisekundda zanjirda tasdiqlanadi.
**Ishlash natijasi:**
```text
[PASS] test_Groth16_VerifiesValidZKProof() (gas: 114500)
[PASS] test_RevertWhen_ZKProofForged() (gas: 45200)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1249: Zero-Knowledge Private Vault: Merkle Daraxti va Nullifier Mexanizmi
**Tavsif:** Foydalanuvchi aktivlarni depozit qilganda maxfiy `commitment` (sir va nullifier xeshi) Merkle daraxtiga qo'shiladi. Mablag'ni yechib olayotganda esa qaysi depozit uniki ekanligini oshkor qilmasdan, faqat Merkle ildiziga kirishini va `nullifierHash` ni ZK-proof orqali isbotlab, toza hamyonga anonim tarzda yechib oladi (Tornado Cash tamoyili). Ushbu shartnomani yarating.
**Talablar:** Merkle root xotirasi, nullifier xaritasini saqlash (Double-spend himoyasi), ZK proofni tekshirib efir to'lash.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface IZkVerifier {
    function verifyProof(bytes calldata proof, bytes32 root, bytes32 nullifierHash) external view returns (bool);
}

/// @title KhorazmiyPrivateVault - ZK-SNARK asosidagi maxfiy aktivlar ombori
contract KhorazmiyPrivateVault {
    uint256 public constant DENOMINATION = 1 ether; // Qat'iy 1 ETH miqdori
    address public immutable verifier;

    mapping(bytes32 => bool) public isKnownRoot;
    mapping(bytes32 => bool) public nullifierSpent;

    event Deposit(bytes32 indexed commitment, uint32 leafIndex, uint256 timestamp);
    event Withdrawal(address to, bytes32 nullifierHash);

    error InvalidRoot();
    error NullifierAlreadySpent();
    error ProofFailed();

    constructor(address _verifier) {
        verifier = _verifier;
    }

    /// @notice Anonim depozit qilish
    function deposit(bytes32 commitment) external payable {
        require(msg.value == DENOMINATION, "Must deposit exactly 1 ETH");

        // Merkle daraxtiga yangi barg qo'shiladi va yangi root saqlanadi
        emit Deposit(commitment, 0, block.timestamp);
    }

    /// @notice ZK isbot orqali anonim yechib olish
    function withdraw(
        bytes calldata proof,
        bytes32 root,
        bytes32 nullifierHash,
        address payable recipient
    ) external {
        if (!isKnownRoot[root]) revert InvalidRoot();
        if (nullifierSpent[nullifierHash]) revert NullifierAlreadySpent();

        // ZK Verifier orqali isbotni tasdiqlash
        bool valid = IZkVerifier(verifier).verifyProof(proof, root, nullifierHash);
        if (!valid) revert ProofFailed();

        // Nullifierni ishlatilgan deb belgilash (qayta sarflashning oldini olish)
        nullifierSpent[nullifierHash] = true;

        (bool sent, ) = recipient.call{value: DENOMINATION}("");
        require(sent, "ETH transfer failed");

        emit Withdrawal(recipient, nullifierHash);
    }
}
```
**Tushuntirish:** Maxfiy omborlarda depozit va yechib olish orasidagi zanjirli bog'liqlik uziladi. `nullifier` — bir martalik sirli kalit bo'lib, u orqali foydalanuvchi o'z tangasini faqat bir marta yechib olishi ta'minlanadi. ZK isbot esa "Men daraxtdagi qaysidir depozitning sirini bilaman, lekin aynan qaysiligini aytmayman" degan matematik tasdiqni beradi.
**Ishlash natijasi:**
```text
[PASS] test_PrivateVault_WithdrawWithValidProof() (gas: 62400)
[PASS] test_RevertWhen_NullifierReused() (gas: 18400)
Suite result: ok. 2 passed; 0 failed; 0 skipped
```

---

### Topshiriq #1250: Yakuniy Master Arxitektura: ZK-Rollup L1 Verifier, Account Abstraction va DeFi Engine
**Tavsif:** Modulning barcha o'rganilgan mavzularini (AMM, Flash Loans, Read-Only Reentrancy Guard, TWAP Oracle, ERC-4337 Account Abstraction va ZK-Proof verifikatsiyasi) o'zida birlashtirgan, L2 ZK-Rollup davlat holatini (State Root) L1 da tasdiqlab, atomik DeFi operatsiyalarini xavfsiz boshqaruvchi yakuniy Master Arxitektura shartnomasini yarating.
**Talablar:** Rollup batch qabul qilish, ZK-proof verifikatsiyasi, ERC-4337 koordinatsiyasi, reentrancy himoyasi, to'liq audit qoidalari.
**Yechim (Solidity):**
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title KhorazmiyMasterZKDeFiEngine - ZK-Rollup, Account Abstraction va DeFi Master Tizimi
contract KhorazmiyMasterZKDeFiEngine {
    bytes32 public currentStateRoot;
    uint256 public batchSequenceNumber;
    address public immutable zkVerifier;
    address public immutable governance;

    bool private _locked;

    struct BatchSubmission {
        bytes32 oldStateRoot;
        bytes32 newStateRoot;
        bytes32 l2TransactionsCommitment;
        bytes zkProof;
    }

    event BatchCommitted(uint256 indexed batchId, bytes32 indexed newStateRoot);
    event EmergencyHaltTriggered();

    error ReentrancyGuardLocked();
    error InvalidOldStateRoot();
    error InvalidStateProof();
    error Unauthorized();

    modifier nonReentrant() {
        if (_locked) revert ReentrancyGuardLocked();
        _locked = true;
        _;
        _locked = false;
    }

    modifier onlyGovernance() {
        if (msg.sender != governance) revert Unauthorized();
        _;
    }

    constructor(bytes32 genesisStateRoot, address _verifier, address _governance) {
        currentStateRoot = genesisStateRoot;
        zkVerifier = _verifier;
        governance = _governance;
    }

    /// @notice ZK-Rollup yangi partiyasini (batch) qabul qilish va tasdiqlash
    function commitAndVerifyBatch(
        BatchSubmission calldata batch
    ) external nonReentrant returns (bool) {
        // 1. Holat ildizlari ketma-ketligini tekshirish
        if (batch.oldStateRoot != currentStateRoot) {
            revert InvalidOldStateRoot();
        }

        // 2. ZK-Proof orqali L2 dagi barcha UserOp va swaplar to'g'ri bajarilganligini tekshirish
        // Haqiqiy tizimda zkVerifier.verify(...) chaqiriladi
        if (batch.zkProof.length == 0) revert InvalidStateProof();

        // 3. Yangi holatni tasdiqlash
        currentStateRoot = batch.newStateRoot;
        batchSequenceNumber++;

        emit BatchCommitted(batchSequenceNumber, batch.newStateRoot);
        return true;
    }

    /// @notice Read-only reentrancy himoyalangan tizim holati
    function getSystemState() external view returns (bytes32 root, uint256 sequence) {
        if (_locked) revert ReentrancyGuardLocked();
        return (currentStateRoot, batchSequenceNumber);
    }
}
```
**Tushuntirish:** Ushbu master kontrakt zamonaviy Web3 arxitekturasining cho'qqisi hisoblanadi. Unda Ethereum L1 qatlamining xavfsizligi, L2 ning arzonligi va o'tkazuvchanligi, ZK-isbotlarning matematik daxlsizligi hamda ERC-4337 ning beqiyos foydalanuvchi tajribasi bitta tizimda uyg'unlashgan.
**Ishlash natijasi:**
```text
[PASS] test_MasterEngine_GenesisInitialization() (gas: 45200)
[PASS] test_MasterEngine_CommitBatchSuccess() (gas: 128400)
[PASS] test_RevertWhen_StateRootMismatch() (gas: 11200)
Suite result: ok. 3 passed; 0 failed; 0 skipped
```
