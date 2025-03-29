[BITS 16]
ORG 0x7e00
dd 4
jmp _main
;!!!!!!!!!!!!!!!!

                %macro Print 1
                    pushad
                    mov al, %1
                    mov ah, 0x9
                    mov bh, 0
                    mov bl, 0x2 ; green
                    mov cx, 1
                    int 0x10
                    popad
                %endmacro
            
%include "InBuiltFunctions_COS/printc.asm"
;CREATE_FUNCTION ['_println', 'void', 'void']
_println:
	;OPENSCOPE ['']
		push ebp
		mov ebp, esp
		;CREATE ['i32', '_#EXP_FUNCTION_ARGUMENT_0']
		sub esp, 4
		;MOV ['_#EXP_FUNCTION_ARGUMENT_0', '10']
		mov dword[ebp + -4], 10
		;CREATE ['UNKNOWN', '_#EXP_FUNCTION_RETURN_1']
		sub esp, 4
		;CALL ['_#EXP_FUNCTION_RETURN_1', '_printc', '_#EXP_FUNCTION_ARGUMENT_0']
		mov eax, dword[ebp + -4]
		push eax
		call _printc
		add esp, 4
		;CREATE ['i32', '_#EXP_FUNCTION_ARGUMENT_2']
		sub esp, 4
		;MOV ['_#EXP_FUNCTION_ARGUMENT_2', '13']
		mov dword[ebp + -12], 13
		;CREATE ['UNKNOWN', '_#EXP_FUNCTION_RETURN_3']
		sub esp, 4
		;CALL ['_#EXP_FUNCTION_RETURN_3', '_printc', '_#EXP_FUNCTION_ARGUMENT_2']
		mov eax, dword[ebp + -12]
		push eax
		call _printc
		add esp, 4
		;CLOSESCOPE ['']
		mov esp, ebp
		pop ebp
	;END_FUNCTION ['']
ret
;CREATE_FUNCTION ['_printb', 'void', 'i32~_number']
_printb:
	;OPENSCOPE ['']
		push ebp
		mov ebp, esp
		;CREATE_ARGUMENT ['i32', '_number']
		sub esp, 4
		mov eax, dword[ebp+6]
		mov dword[ebp + -4], eax
		;CREATE ['i32', '_#EXP_FUNCTION_ARGUMENT_4']
		sub esp, 4
		;MOV ['_#EXP_FUNCTION_ARGUMENT_4', '48']
		mov dword[ebp + -8], 48
		;CREATE ['UNKNOWN', '_#EXP_FUNCTION_RETURN_5']
		sub esp, 4
		;CALL ['_#EXP_FUNCTION_RETURN_5', '_printc', '_#EXP_FUNCTION_ARGUMENT_4']
		mov eax, dword[ebp + -8]
		push eax
		call _printc
		add esp, 4
		;CREATE ['i32', '_#EXP_FUNCTION_ARGUMENT_6']
		sub esp, 4
		;MOV ['_#EXP_FUNCTION_ARGUMENT_6', '98']
		mov dword[ebp + -16], 98
		;CREATE ['UNKNOWN', '_#EXP_FUNCTION_RETURN_7']
		sub esp, 4
		;CALL ['_#EXP_FUNCTION_RETURN_7', '_printc', '_#EXP_FUNCTION_ARGUMENT_6']
		mov eax, dword[ebp + -16]
		push eax
		call _printc
		add esp, 4
		;CREATE ['i32', '_counter', '1']
		sub esp, 4
		;CREATE ['i32', 'EXP_TEMP_VAR_0', '1']
		sub esp, 4
		;MOV ['EXP_TEMP_VAR_0', '0']
		mov dword[ebp + -28], 0
		;MOV ['_counter', 'EXP_TEMP_VAR_0']
		mov eax, dword[ebp + -28]
		mov dword[ebp + -24], eax
		;REPEAT ['rep_0']
		repeat_0:
		;OPENSCOPE ['']
			push ebp
			mov ebp, esp
			;CREATE ['UNKNOWN', 'EXP_VAR_0']
			sub esp, 4
			;CREATE ['i32', 'EXP_VAR_1']
			sub esp, 4
			;* ['EXP_VAR_1', '4', '8']
			mov eax, 4
			imul eax, 8
			mov dword[ebp + -8], eax
			;< ['EXP_VAR_0', '_counter', 'EXP_VAR_1']
			mov eax, dword[ebp + -8]
			cmp dword[ebp + 8], eax
			setl byte[ebp + -4]
			;! ['EXP_VAR_0']
			not dword[ebp + -4]
			and dword[ebp + -4], 1
			;IF ['EXP_VAR_0']
			cmp dword[ebp + -4], 0
			je endif_0
			;OPENSCOPE ['']
				push ebp
				mov ebp, esp
				;BREAK ['rep_0']
				mov esp, ebp
				pop ebp
				mov esp, ebp
				pop ebp
				jmp endRepeat_0
				;CLOSESCOPE ['']
				mov esp, ebp
				pop ebp
			;ENDIF ['']
			endif_0:
			;CREATE ['i32', '_bit', '1']
			sub esp, 4
			;CREATE ['UNKNOWN', 'EXP_TEMP_VAR_1', '1']
			sub esp, 4
			;&& ['EXP_TEMP_VAR_1', '_number', '1']
			mov eax, dword[ebp + 28]
			and eax, 1
			mov dword[ebp + -16], eax
			;MOV ['_bit', 'EXP_TEMP_VAR_1']
			mov eax, dword[ebp + -16]
			mov dword[ebp + -12], eax
			;CREATE ['UNKNOWN', 'EXP_TEMP_VAR_2', '1']
			sub esp, 4
			;>> ['EXP_TEMP_VAR_2', '_number', '1']
			mov eax, dword[ebp + 28]
			shr eax, 1
			mov dword[ebp + -20], eax
			;MOV ['_number', 'EXP_TEMP_VAR_2']
			mov eax, dword[ebp + -20]
			mov dword[ebp + 28], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_3', '1']
			sub esp, 4
			;+ ['EXP_TEMP_VAR_3', '_counter', '1']
			mov eax, dword[ebp + 8]
			add eax, 1
			mov dword[ebp + -24], eax
			;MOV ['_counter', 'EXP_TEMP_VAR_3']
			mov eax, dword[ebp + -24]
			mov dword[ebp + 8], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_4', '1']
			sub esp, 4
			;+ ['EXP_TEMP_VAR_4', '_bit', '48']
			mov eax, dword[ebp + -12]
			add eax, 48
			mov dword[ebp + -28], eax
			;MOV ['_bit', 'EXP_TEMP_VAR_4']
			mov eax, dword[ebp + -28]
			mov dword[ebp + -12], eax
			;CREATE ['i32', '_#EXP_FUNCTION_ARGUMENT_8']
			sub esp, 4
			;MOV ['_#EXP_FUNCTION_ARGUMENT_8', '_bit']
			mov eax, dword[ebp + -12]
			mov dword[ebp + -32], eax
			;CREATE ['UNKNOWN', '_#EXP_FUNCTION_RETURN_9']
			sub esp, 4
			;CALL ['_#EXP_FUNCTION_RETURN_9', '_printc', '_#EXP_FUNCTION_ARGUMENT_8']
			mov eax, dword[ebp + -32]
			push eax
			call _printc
			add esp, 4
			;CLOSESCOPE ['']
			mov esp, ebp
			pop ebp
		;ENDREPEAT ['']
		jmp repeat_0
		endRepeat_0:
		;CLOSESCOPE ['']
		mov esp, ebp
		pop ebp
	;END_FUNCTION ['']
ret
;CREATE_FUNCTION ['_printn', 'void', 'i32~_number']
_printn:
	;OPENSCOPE ['']
		push ebp
		mov ebp, esp
		;CREATE_ARGUMENT ['i32', '_number']
		sub esp, 4
		mov eax, dword[ebp+6]
		mov dword[ebp + -4], eax
		;CREATE ['i32', '_buffer', '11']
		sub esp, 44
		;CREATE ['i32', 'EXP_TEMP_VAR_5', '1']
		sub esp, 4
		;MOV ['EXP_TEMP_VAR_5', '0']
		mov dword[ebp + -52], 0
		;OPENSCOPE ['']
			push ebp
			mov ebp, esp
			;CREATE ['i32', 'IR_OPT_0']
			sub esp, 4
			;MOV ['IR_OPT_0', '0']
			mov dword[ebp + -4], 0
			;REPEAT ['IR_OPT_2']
			repeat_1:
			;OPENSCOPE ['']
				push ebp
				mov ebp, esp
				;CREATE ['i32', 'IR_OPT_1']
				sub esp, 4
				;MOV ['IR_OPT_1', 'IR_OPT_0']
				mov eax, dword[ebp + 4]
				mov dword[ebp + -4], eax
				;== ['IR_OPT_1', 'IR_OPT_1', '44']
				cmp dword[ebp + -4], 44
				sete byte[ebp + -4]
				;IF ['IR_OPT_1']
				cmp dword[ebp + -4], 0
				je endif_1
				;OPENSCOPE ['']
					push ebp
					mov ebp, esp
					;BREAK ['IR_OPT_2']
					mov esp, ebp
					pop ebp
					mov esp, ebp
					pop ebp
					jmp endRepeat_1
					;CLOSESCOPE ['']
					mov esp, ebp
					pop ebp
				;ENDIF ['']
				endif_1:
				;MOV ['_buffer', 'EXP_TEMP_VAR_5', 'IR_OPT_0']
				mov eax, dword[ebp + 8]
				mov edi, ebp
				add edi, 52
				sub edi, dword[ebp + 4]
				mov dword[edi], eax
				;+ ['IR_OPT_0', 'IR_OPT_0', '4']
				mov eax, dword[ebp + 4]
				add eax, 4
				mov dword[ebp + 4], eax
				;CLOSESCOPE ['']
				mov esp, ebp
				pop ebp
			;ENDREPEAT ['']
			jmp repeat_1
			endRepeat_1:
			;CLOSESCOPE ['']
			mov esp, ebp
			pop ebp
		;CREATE ['i32', '_pointer', '1']
		sub esp, 4
		;CREATE ['i32', 'EXP_TEMP_VAR_6', '1']
		sub esp, 4
		;MOV ['EXP_TEMP_VAR_6', '10']
		mov dword[ebp + -60], 10
		;MOV ['_pointer', 'EXP_TEMP_VAR_6']
		mov eax, dword[ebp + -60]
		mov dword[ebp + -56], eax
		;CREATE ['i32', '_runOnceFlag', '1']
		sub esp, 4
		;CREATE ['i32', 'EXP_TEMP_VAR_7', '1']
		sub esp, 4
		;MOV ['EXP_TEMP_VAR_7', '1']
		mov dword[ebp + -68], 1
		;MOV ['_runOnceFlag', 'EXP_TEMP_VAR_7']
		mov eax, dword[ebp + -68]
		mov dword[ebp + -64], eax
		;REPEAT ['rep_1']
		repeat_2:
		;OPENSCOPE ['']
			push ebp
			mov ebp, esp
			;CREATE ['UNKNOWN', 'EXP_VAR_2']
			sub esp, 4
			;CREATE ['i32', 'EXP_VAR_3']
			sub esp, 4
			;!= ['EXP_VAR_3', '_number', '0']
			cmp dword[ebp + 68], 0
			setne byte[ebp + -8]
			;CREATE ['i32', 'EXP_VAR_4']
			sub esp, 4
			;== ['EXP_VAR_4', '_runOnceFlag', '1']
			cmp dword[ebp + 8], 1
			sete byte[ebp + -12]
			;or ['EXP_VAR_2', 'EXP_VAR_3', 'EXP_VAR_4']
			mov eax, dword[ebp + -8]
			or eax, dword[ebp + -12]
			mov dword[ebp + -4], eax
			;! ['EXP_VAR_2']
			not dword[ebp + -4]
			and dword[ebp + -4], 1
			;IF ['EXP_VAR_2']
			cmp dword[ebp + -4], 0
			je endif_2
			;OPENSCOPE ['']
				push ebp
				mov ebp, esp
				;BREAK ['rep_1']
				mov esp, ebp
				pop ebp
				mov esp, ebp
				pop ebp
				jmp endRepeat_2
				;CLOSESCOPE ['']
				mov esp, ebp
				pop ebp
			;ENDIF ['']
			endif_2:
			;CREATE ['i32', '_digit', '1']
			sub esp, 4
			;CREATE ['i32', 'EXP_TEMP_VAR_8', '1']
			sub esp, 4
			;% ['EXP_TEMP_VAR_8', '_number', '10']
			mov eax, dword[ebp + 68]
			mov ebx, 10
			xor edx, edx
			idiv ebx
			mov dword[ebp + -20], edx
			;MOV ['_digit', 'EXP_TEMP_VAR_8']
			mov eax, dword[ebp + -20]
			mov dword[ebp + -16], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_9', '1']
			sub esp, 4
			;/ ['EXP_TEMP_VAR_9', '_number', '10']
			mov eax, dword[ebp + 68]
			mov ebx, 10
			xor edx, edx
			idiv ebx
			mov dword[ebp + -24], eax
			;MOV ['_number', 'EXP_TEMP_VAR_9']
			mov eax, dword[ebp + -24]
			mov dword[ebp + 68], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_10', '1']
			sub esp, 4
			;MOV ['EXP_TEMP_VAR_10', '_pointer']
			mov eax, dword[ebp + 16]
			mov dword[ebp + -28], eax
			;* ['EXP_TEMP_VAR_10', 'EXP_TEMP_VAR_10', '4']
			mov eax, dword[ebp + -28]
			imul eax, 4
			mov dword[ebp + -28], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_11', '1']
			sub esp, 4
			;+ ['EXP_TEMP_VAR_11', '_digit', '48']
			mov eax, dword[ebp + -16]
			add eax, 48
			mov dword[ebp + -32], eax
			;MOV ['_buffer', 'EXP_TEMP_VAR_11', 'EXP_TEMP_VAR_10']
			mov eax, dword[ebp + -32]
			mov edi, ebp
			add edi, 64
			sub edi, dword[ebp + -28]
			mov dword[edi], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_12', '1']
			sub esp, 4
			;- ['EXP_TEMP_VAR_12', '_pointer', '1']
			mov eax, dword[ebp + 16]
			sub eax, 1
			mov dword[ebp + -36], eax
			;MOV ['_pointer', 'EXP_TEMP_VAR_12']
			mov eax, dword[ebp + -36]
			mov dword[ebp + 16], eax
			;CREATE ['i32', 'EXP_TEMP_VAR_13', '1']
			sub esp, 4
			;MOV ['EXP_TEMP_VAR_13', '0']
			mov dword[ebp + -40], 0
			;MOV ['_runOnceFlag', 'EXP_TEMP_VAR_13']
			mov eax, dword[ebp + -40]
			mov dword[ebp + 8], eax
			;CLOSESCOPE ['']
			mov esp, ebp
			pop ebp
		;ENDREPEAT ['']
		jmp repeat_2
		endRepeat_2:
		;CREATE ['i32', 'EXP_TEMP_VAR_14', '1']
		sub esp, 4
		;+ ['EXP_TEMP_VAR_14', '_pointer', '1']
		mov eax, dword[ebp + -56]
		add eax, 1
		mov dword[ebp + -72], eax
		;MOV ['_pointer', 'EXP_TEMP_VAR_14']
		mov eax, dword[ebp + -72]
		mov dword[ebp + -56], eax
		;REPEAT ['rep_2']
		repeat_3:
		;OPENSCOPE ['']
			push ebp
			mov ebp, esp
			;CREATE ['UNKNOWN', 'EXP_VAR_5']
			sub esp, 4
			;< ['EXP_VAR_5', '_pointer', '11']
			cmp dword[ebp + 20], 11
			setl byte[ebp + -4]
			;! ['EXP_VAR_5']
			not dword[ebp + -4]
			and dword[ebp + -4], 1
			;IF ['EXP_VAR_5']
			cmp dword[ebp + -4], 0
			je endif_3
			;OPENSCOPE ['']
				push ebp
				mov ebp, esp
				;BREAK ['rep_2']
				mov esp, ebp
				pop ebp
				mov esp, ebp
				pop ebp
				jmp endRepeat_3
				;CLOSESCOPE ['']
				mov esp, ebp
				pop ebp
			;ENDIF ['']
			endif_3:
			;CREATE ['i32', '_#EXP_FUNCTION_ARGUMENT_10']
			sub esp, 4
			;CREATE ['i32', '_#EXP_INDEX_10']
			sub esp, 4
			;MOV ['_#EXP_INDEX_10', '_pointer']
			mov eax, dword[ebp + 20]
			mov dword[ebp + -12], eax
			;* ['_#EXP_INDEX_10', '_#EXP_INDEX_10', '4']
			mov eax, dword[ebp + -12]
			imul eax, 4
			mov dword[ebp + -12], eax
			;MOV ['_#EXP_INDEX_10', '_buffer', '_#EXP_INDEX_10']
			mov edi, ebp
			add edi, 68
			sub edi, dword[ebp + -12]
			mov edi, dword[edi]
			mov dword[ebp + -12], edi
			;MOV ['_#EXP_FUNCTION_ARGUMENT_10', '_#EXP_INDEX_10']
			mov eax, dword[ebp + -12]
			mov dword[ebp + -8], eax
			;CREATE ['UNKNOWN', '_#EXP_FUNCTION_RETURN_12']
			sub esp, 4
			;CALL ['_#EXP_FUNCTION_RETURN_12', '_printc', '_#EXP_FUNCTION_ARGUMENT_10']
			mov eax, dword[ebp + -8]
			push eax
			call _printc
			add esp, 4
			;CREATE ['i32', 'EXP_TEMP_VAR_15', '1']
			sub esp, 4
			;+ ['EXP_TEMP_VAR_15', '_pointer', '1']
			mov eax, dword[ebp + 20]
			add eax, 1
			mov dword[ebp + -20], eax
			;MOV ['_pointer', 'EXP_TEMP_VAR_15']
			mov eax, dword[ebp + -20]
			mov dword[ebp + 20], eax
			;CLOSESCOPE ['']
			mov esp, ebp
			pop ebp
		;ENDREPEAT ['']
		jmp repeat_3
		endRepeat_3:
		;CLOSESCOPE ['']
		mov esp, ebp
		pop ebp
	;END_FUNCTION ['']
ret
;CREATE_FUNCTION ['_prints', 'void', 'i32~_ptr']
_prints:
	;OPENSCOPE ['']
		push ebp
		mov ebp, esp
		;CREATE_ARGUMENT ['i32', '_ptr']
		sub esp, 4
		mov eax, dword[ebp+6]
		mov dword[ebp + -4], eax
		;CLOSESCOPE ['']
		mov esp, ebp
		pop ebp
	;END_FUNCTION ['']
ret
times 512*4-($-$$) db 0

;--CONSTANTS--
