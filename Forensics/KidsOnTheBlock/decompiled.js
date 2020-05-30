contract Contract {
    function main() {
        memory[0x40:0x60] = 0x60;
        var var0 = msg.data[0x00:0x20] / 0x0100000000000000000000000000000000000000000000000000000000 & 0xffffffff;
    
        if (var0 == 0x12065fe0) {
            // Dispatch table entry for getBalance()
            if (msg.value) { assert(); }
        
            var var1 = 0x0061;
            var1 = getBalance();
            var temp0 = memory[0x40:0x60];
            memory[temp0:temp0 + 0x20] = var1;
            var temp1 = memory[0x40:0x60];
            return memory[temp1:temp1 + (temp0 + 0x20) - temp1];
        } else if (var0 == 0xd0e30db0) {
            // Dispatch table entry for deposit()
            var1 = 0x007f;
            deposit();
            stop();
        } else if (var0 == 0xf3fef3a3) {
            // Dispatch table entry for withdraw(address,uint256)
            if (msg.value) { assert(); }
        
            var1 = 0x00be;
            var var2 = msg.data[0x04:0x24] & 0xffffffffffffffffffffffffffffffffffffffff;
            var var3 = msg.data[0x24:0x44];
            withdraw(var2, var3);
            stop();
        } else { assert(); }
    }
    
    function getBalance() returns (var r0) {
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x00;
        return storage[keccak256(memory[0x00:0x40])];
    }
    
    function deposit() {
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x00;
        var temp0 = keccak256(memory[0x00:0x40]);
        storage[temp0] = storage[temp0] + msg.value;
    }
    
    function withdraw(var arg0, var arg1) {
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x00;
    
        if (storage[keccak256(memory[0x00:0x40])] < arg1) { revert(memory[0x00:0x00]); }
    
        var temp0 = arg1;
        memory[0x00:0x20] = msg.sender;
        memory[0x20:0x40] = 0x00;
        var temp1 = keccak256(memory[0x00:0x40]);
        storage[temp1] = storage[temp1] - temp0;
        var temp2 = memory[0x40:0x60];
        var temp3;
        temp3, memory[temp2:temp2 + 0x00] = address(arg0 & 0xffffffffffffffffffffffffffffffffffffffff).call.gas(!temp0 * 0x08fc).value(temp0)(memory[temp2:temp2 + memory[0x40:0x60] - temp2]);
    
        if (temp3) { return; }
        else { assert(); }
    }
}
