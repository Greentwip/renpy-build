#include <sys/syscall.h>
#include <linux/memfd.h>


#if defined(ANDROID) || defined(__ANDROID__) // Ugly patch
static int memfd_create(const char *uname, unsigned int flag)
{
#ifdef SYS_memfd_create
	return syscall(SYS_memfd_create, uname, flag);
#else
	return -ENOSYS;
#endif
}
#endif